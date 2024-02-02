from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from user_management.managers.user import UserManager


class User(AbstractUser):
    """
    Customized user model.

    Overrides the parent model to use field `email` as the "username-field".
    """

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
