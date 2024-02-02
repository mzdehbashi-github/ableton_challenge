from typing import Optional

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.authtoken.models import Token
from result import Ok, Result, Err

from ableton_challenge.errors import UnprocessableContent
from user_management.models.user import User
from user_management.models.email_confirmation import EmailConfirmation
from user_management.services.email_confirmation import send_email_confirmation_email


def signup(email: str, password: str) -> Result[User, APIException]:
    if User.objects.filter(email=email).exists():
        return Err(UnprocessableContent(detail=_('User with this email already exists')))
    user = User.objects.create_user(
        email=email,
        password=password
    )

    send_email_confirmation_email(user.email, user.id)
    return Ok(user)


def login(email: str, password: str) -> Result[User, APIException]:
    bad_credentials_error = Err(AuthenticationFailed(detail=_('Unable to log in with provided credentials.')))

    try:
        user = User.objects.select_related('emailconfirmation').get(email=email)
    except User.DoesNotExist:
        return bad_credentials_error
    else:
        if not user.check_password(password):
            return bad_credentials_error
        elif not user.is_active:
            user_deactivated_error = Err(
                UnprocessableContent(detail=_('User is not active.')))

            if not user.emailconfirmation.confirmed_at:
                user_deactivated_error = Err(
                    UnprocessableContent(
                        detail=_('User is not active. please make sure that you have confirmed you email'))
                )

            return user_deactivated_error
        else:
            Token.objects.get_or_create(user=user)
            return Ok(user)


def resend_email_confirmation(email: str) -> Result[Optional[EmailConfirmation], APIException]:
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Ok(None)
    else:
        return send_email_confirmation_email(email, user.id)


def confirm_email(email: str, code: str) -> Result[User, APIException]:
    with transaction.atomic():
        try:
            user = User.objects.select_related().get(email=email)
        except User.DoesNotExist:
            # Maybe it is a good idea to add some logs later, to trace non-existing emails
            return Err(UnprocessableContent(detail=_('Could not confirm email')))
        else:
            try:
                email_confirmation = EmailConfirmation.objects.select_for_update().get(
                    user__email=email,
                    code=code,
                )
            except EmailConfirmation.DoesNotExist:
                return Err(UnprocessableContent(detail=_('Could not confirm email')))
            else:
                if email_confirmation.confirmed_at:
                    return Err(UnprocessableContent(detail=_('Email already confirmed')))

                email_confirmation.confirmed_at = timezone.now()
                email_confirmation.save(update_fields=('confirmed_at',))
                user.is_active = True
                user.save(update_fields=('is_active',))
                return Ok(user)
