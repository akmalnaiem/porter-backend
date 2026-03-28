from django.urls import path
from .views.auth_views import RegisterView
from .views.otp_views import SendOTPView, VerifyOTPView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    # path("login/", LoginView.as_view()),
    path("otp/send/", SendOTPView.as_view()),
    path("otp/verify/", VerifyOTPView.as_view()),
    # path("password/reset/", ResetPasswordView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]