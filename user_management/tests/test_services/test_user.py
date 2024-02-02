from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from user_management.models.email_confirmation import EmailConfirmation
from user_management.models.user import User
from user_management.tests.factories.user import UserFactory
from user_management.tests.factories.email_confirmation import EmailConfirmationFactory
from ableton_challenge.errors import UnprocessableContent
from user_management.services.user import signup, login, confirm_email, resend_email_confirmation


class SignupTestCase(TestCase):

    def test_signup_success(self):
        email = 'test@example.com'
        password = 'testpassword'

        # Call the signup function
        result = signup(email, password)

        # Check if the signup was successful
        self.assertTrue(result.is_ok())

        # Check if email confirmation was sent
        user = User.objects.get(email=email)
        self.assertFalse(user.is_active)
        self.assertTrue(EmailConfirmation.objects.filter(user=user).exists())

    def test_signup_existing_user(self):
        # Create a user with the given email
        existing_user = UserFactory()

        # Call the signup function with the same email
        result = signup(existing_user.email, 'testpassword')

        # Check if the signup failed as expected
        self.assertTrue(result.is_err())
        self.assertIsInstance(result.value, UnprocessableContent)
        self.assertEqual(result.err().detail, 'User with this email already exists')


class LoginTestCase(TestCase):

    def setUp(self):
        self.password = 'testpassword'
        self.email = 'test@example.com'
        self.user = UserFactory(email=self.email, password=self.password, is_active=True)
        self.token = Token.objects.create(user=self.user)

    def test_login_success(self):
        self.user.save()
        email = 'test@example.com'
        password = self.password

        # Call the login function
        result = login(email, password)

        # Check if the login was successful
        self.assertTrue(result.is_ok())
        self.assertEqual(result.value, self.user)
        self.assertTrue(Token.objects.filter(user=self.user).exists())

    def test_login_invalid_credentials(self):
        # Call the login function with invalid credentials
        result = login('test@example.com', 'wrongpassword')

        # Check if the login failed as expected
        self.assertTrue(result.is_err())
        self.assertIsInstance(result.value, AuthenticationFailed)
        self.assertEqual(result.err().detail, 'Unable to log in with provided credentials.')

    def test_login_inactive_user(self):
        # Deactivate the user
        self.user.is_active = False
        self.user.save()

        # User confirmed their email previously
        EmailConfirmationFactory(user=self.user, confirmed_at=timezone.now())

        # Call the login function with inactive user
        result = login(self.email, self.password)

        # Check if the login failed as expected
        self.assertTrue(result.is_err())
        self.assertIsInstance(result.value, UnprocessableContent)
        self.assertEqual(result.err().detail, 'User is not active.')

    def test_login_inactive_user_unconfirmed_email(self):
        # Deactivate the user
        self.user.is_active = False
        self.user.save()

        # User did NOT confirm their email previously
        EmailConfirmationFactory(user=self.user)

        # Call the login function with inactive user and unconfirmed email
        result = login('test@example.com', self.password)

        # Check if the login failed as expected
        self.assertTrue(result.is_err())
        self.assertIsInstance(result.value, UnprocessableContent)
        self.assertEqual(
            result.err().detail,
            'User is not active. please make sure that you have confirmed you email'
        )


class ConfirmEmailTestCase(TestCase):

    def setUp(self):
        self.email_confirmation = EmailConfirmationFactory()

    def test_confirm_email_success(self):
        email = self.email_confirmation.user.email
        code = self.email_confirmation.code

        # Call the confirm_email function
        result = confirm_email(email, code)
        self.email_confirmation.refresh_from_db()

        # Check if the email confirmation was successful
        self.assertTrue(result.is_ok())
        self.assertTrue(self.email_confirmation.user.is_active)
        self.assertIsNotNone(self.email_confirmation.confirmed_at)

    def test_confirm_email_invalid_code(self):
        # Call the confirm_email function with invalid code
        result = confirm_email('test@example.com', 'invalidcode')

        # Check if the confirmation failed as expected
        self.assertTrue(result.is_err())
        self.assertEqual(result.err().detail, 'Could not confirm email')

    def test_confirm_email_already_confirmed(self):
        # Mark the email as already confirmed
        self.email_confirmation.confirmed_at = timezone.now()
        self.email_confirmation.save()

        # Call the confirm_email function for an already confirmed email
        email = self.email_confirmation.user.email
        code = self.email_confirmation.code
        result = confirm_email(email, code)

        # Check if the confirmation failed as expected
        self.assertTrue(result.is_err())
        self.assertEqual(result.err().detail, 'Email already confirmed')

    def test_confirm_email_non_existing_email(self):
        # Call the confirm_email function with non-existing email
        code = self.email_confirmation.code
        result = confirm_email('nonexisting@example.com', code)

        # Check if the confirmation failed as expected
        self.assertTrue(result.is_err())
        self.assertEqual(result.err().detail, 'Could not confirm email')


class ResendEmailConfirmationTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_resend_email_confirmation_success(self):
        email = self.user.email

        # Call the resend_email_confirmation function
        result = resend_email_confirmation(email)

        # Check if the email confirmation resend was successful
        self.assertTrue(result.is_ok())
        self.assertIsInstance(result.value, EmailConfirmation)
        self.assertEqual(result.value.user, self.user)
        # You may need to adjust assertions according to your implementation of send_email_confirmation_email

    def test_resend_email_confirmation_non_existing_email(self):
        # Call the resend_email_confirmation function with non-existing email

        non_existing_email = 'nonexisting@example.com'
        result = resend_email_confirmation(non_existing_email)

        # Check if the resend failed as expected
        self.assertTrue(result.is_ok())
        self.assertIsNone(result.value)

        self.assertFalse(EmailConfirmation.objects.filter(user__email=non_existing_email).exists())
