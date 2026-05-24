from django.urls import path
from .views.auth_views import PublicTokenRefreshView, UserRegisterView, PorterRegisterView
from .views.otp_views import SendOTPView, UserVerifyOTPView, PorterVerifyOTPView

urlpatterns = [
    path("user/register/", UserRegisterView.as_view()),
    path("porter/register/", PorterRegisterView.as_view()),
    # path("login/", LoginView.as_view()),
    path("otp/send/", SendOTPView.as_view()),
    path("user/otp/verify/", UserVerifyOTPView.as_view()),
    path("porter/otp/verify/", PorterVerifyOTPView.as_view()),
    # path("password/reset/", ResetPasswordView.as_view()),
    path("token/refresh/", PublicTokenRefreshView.as_view(), name="token_refresh"),
]
