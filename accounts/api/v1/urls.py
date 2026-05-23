from django.urls import path
from .views.auth_views import RegisterView, PublicTokenRefreshView
from .views.otp_views import SendOTPView, VerifyOTPView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    # path("login/", LoginView.as_view()),
    path("otp/send/", SendOTPView.as_view()),
    path("otp/verify/", VerifyOTPView.as_view()),
    # path("password/reset/", ResetPasswordView.as_view()),
    path("token/refresh/", PublicTokenRefreshView.as_view(), name="token_refresh"),
]
