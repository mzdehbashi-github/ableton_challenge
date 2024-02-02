from random import randint

from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import transaction
from result import Ok, Err, Result
from rest_framework.exceptions import APIException

from user_management.models.email_confirmation import EmailConfirmation
from ableton_challenge.errors import UnprocessableContent


def send_email_confirmation_email(email: str, user_id: int) -> Result[EmailConfirmation, APIException]:
    """
    Sends an email confirmation email to the specified user.

    Workflow:
        Tries to retrieve an existing EmailConfirmation object for the user.
           - If the object doesn't exist, creates a new one.
           - If the object exists, updates its code and expiration time.
           - Finally sends the email.

        If the user's email is already confirmed, returns an error indicating that the email is already confirmed.

    Caveat: This function always assume that the user exists.
    """
    code = str(randint(10000, 99999))
    expires_at = timezone.now() + timezone.timedelta(hours=1)
    with transaction.atomic():
        try:
            email_confirmation = EmailConfirmation.objects.select_for_update().get(user__email=email)
        except EmailConfirmation.DoesNotExist:
            email_confirmation = EmailConfirmation.objects.create(
                code=code,
                user_id=user_id,
                expires_at=expires_at,
            )
        else:
            if email_confirmation.confirmed_at:
                return Err(UnprocessableContent(detail=_('Email is already confirmed for this user')))

            email_confirmation.code = code
            email_confirmation.expires_at = expires_at
            email_confirmation.save(update_fields=('code', 'expires_at'))

        send_mail(
            _('Email Confirmation'),
            _('Please click here to confirm your email {}').format(email_confirmation.code),
            "from@example.com",
            [email],
            fail_silently=False,
        )

        return Ok(email_confirmation)
