from django.urls import path
from rest_framework import routers

from user_management.views import v1

router = routers.SimpleRouter()
router.register('v1/users/signup', v1.SignupView)
router.register('v1/users/login', v1.LoginView)
urlpatterns = router.urls
urlpatterns += [
    path('v1/users/resend-email-confirmation', v1.resend_email_confirmation_view),
    path('v1/users/confirm-email', v1.confirm_email_view),
]
