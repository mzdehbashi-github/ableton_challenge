from django.db import models


class EmailConfirmation(models.Model):
    user = models.OneToOneField('user_management.User', primary_key=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    expires_at = models.DateTimeField()
    confirmed_at = models.DateTimeField(null=True, blank=True)
