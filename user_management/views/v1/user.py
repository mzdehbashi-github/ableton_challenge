from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from user_management.models.user import User
from user_management.serializers.v1.user import SignupSerializer, LoginSerializer
from user_management.serializers.v1.user import ResendEmailConfirmationSerializer, ConfirmEmailSerializer
from user_management.services.user import signup, login, resend_email_confirmation, confirm_email


class SignupView(GenericViewSet, CreateModelMixin):
    queryset = User.objects
    permission_classes = []
    authentication_classes = []
    serializer_class = SignupSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        result = signup(email, password)
        if result.is_err():
            raise result.err()

        serializer.instance = result.value


class LoginView(GenericViewSet, CreateModelMixin):
    queryset = User.objects
    permission_classes = []
    authentication_classes = []
    serializer_class = LoginSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        result = login(email, password)
        if result.is_err():
            raise result.err()

        serializer.instance = result.value


@swagger_auto_schema(
    methods=['POST'],
    request_body=ResendEmailConfirmationSerializer,
    responses={200: None}
)
@api_view(['POST'])
@permission_classes([])
def resend_email_confirmation_view(request):
    serializer = ResendEmailConfirmationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data['email']
        result = resend_email_confirmation(email)
        if result.is_err():
            raise result.err()

        return Response(status=status.HTTP_200_OK)


@swagger_auto_schema(
    methods=['POST'],
    request_body=ConfirmEmailSerializer,
    responses={200: None}
)
@api_view(['POST'])
@permission_classes([])
def confirm_email_view(request):
    serializer = ConfirmEmailSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        result = confirm_email(email, code)
        if result.is_err():
            raise result.err()

        return Response(status=status.HTTP_200_OK)
