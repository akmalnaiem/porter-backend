from django.urls import path
from .views.auth_views import PublicTokenRefreshView, UserRegisterView, PorterRegisterView
from .views.otp_views import SendOTPView, UserVerifyOTPView, PorterVerifyOTPView
from .views.profile_views import ProfileView, ProfileUpdateView

urlpatterns = [
    # Registration
    path("user/register/", UserRegisterView.as_view()),
    path("porter/register/", PorterRegisterView.as_view()),
    # path("login/", LoginView.as_view()),

    # OTP
    path("otp/send/", SendOTPView.as_view()),
    path("user/otp/verify/", UserVerifyOTPView.as_view()),
    path("porter/otp/verify/", PorterVerifyOTPView.as_view()),
    # path("password/reset/", ResetPasswordView.as_view()),

    # JWT Token_refresh
    path("token/refresh/", PublicTokenRefreshView.as_view(), name="token_refresh"),

    # Profile
    path("profile/", ProfileView.as_view()),
    path("profile/update/", ProfileUpdateView.as_view()),
]
