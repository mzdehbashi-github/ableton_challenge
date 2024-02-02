from django.contrib import admin

from user_management.models.email_confirmation import EmailConfirmation


@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'code',
        'expires_at',
        'confirmed_at',
    ]
