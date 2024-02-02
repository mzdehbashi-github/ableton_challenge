from django.test import TestCase
from django.utils import timezone

from ableton_challenge.errors import UnprocessableContent
from user_management.services.email_confirmation import send_email_confirmation_email
from user_management.models.email_confirmation import EmailConfirmation
from user_management.tests.factories.user import UserFactory
from user_management.tests.factories.email_confirmation import EmailConfirmationFactory


class SendEmailConfirmationEmailTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_send_email_confirmation_email_success(self):
        email = self.user.email

        # Call the send_email_confirmation_email function
        result = send_email_confirmation_email(email, self.user.id)

        # Check if the email confirmation email sending was successful
        self.assertTrue(result.is_ok())
        self.assertIsInstance(result.value, EmailConfirmation)
        self.assertEqual(result.value.user, self.user)

    def test_send_email_confirmation_email_already_confirmed(self):
        # Mark the email as already confirmed
        EmailConfirmationFactory(user=self.user, confirmed_at=timezone.now())

        email = self.user.email
        user_id = self.user.id
        # Call the send_email_confirmation_email function for an already confirmed email
        result = send_email_confirmation_email(email, user_id)

        # Check if the sending failed as expected
        self.assertTrue(result.is_err())
        self.assertIsInstance(result.value, UnprocessableContent)
        self.assertEqual(result.err().detail, 'Email is already confirmed for this user')

    def test_send_email_confirmation_email_already_exists_but_not_confirmed(self):
        # Mark the email as already confirmed
        email_confirmation = EmailConfirmationFactory(user=self.user)
        initial_code = email_confirmation.code

        email = self.user.email
        user_id = self.user.id
        # Call the send_email_confirmation_email function for an already confirmed email
        result = send_email_confirmation_email(email, user_id)

        # Check if the sending failed as expected
        self.assertTrue(result.is_ok())
        self.assertIsInstance(result.value, EmailConfirmation)
        self.assertIsNotNone(result.value.code)
        self.assertNotEqual(result.value.code, initial_code)
