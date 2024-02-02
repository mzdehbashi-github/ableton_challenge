from rest_framework import serializers

from user_management.models.user import User


class SignupSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(source='auth_token.key', read_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'token',
        )


class ResendEmailConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ConfirmEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=5)
