import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import OTP, User
from accounts.tests.helpers import (
    VALID_OTP_CODE,
    VALID_PHONE_E164,
    VALID_PHONE_RAW,
    accounts_url,
    create_otp_record,
    create_user,
    make_registration_temp_token,
)

MINIMAL_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


@pytest.mark.django_db
class TestUserRegisterAPI:
    def test_register_missing_temp_token_returns_404(self, client):
        response = client.post(
            accounts_url("user/register/"),
            {"full_name": "New User"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"] == "Temp token required"

    def test_register_invalid_temp_token(self, client):
        response = client.post(
            accounts_url("user/register/"),
            {
                "temp_token": make_registration_temp_token(invalid=True),
                "full_name": "New User",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Invalid token"

    def test_register_expired_temp_token(self, client):
        response = client.post(
            accounts_url("user/register/"),
            {
                "temp_token": make_registration_temp_token(expired=True),
                "full_name": "New User",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["error"] == "Token expired"

    def test_register_success_creates_user_and_tokens(self, client):
        token = make_registration_temp_token()

        response = client.post(
            accounts_url("user/register/"),
            {
                "temp_token": token,
                "full_name": "New User",
                "email": "newuser@example.com",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"]["full_name"] == "New User"
        assert response.data["user"]["phone_number"] == VALID_PHONE_E164
        assert response.data["user"]["email"] == "newuser@example.com"
        assert response.data["user"]["role"] == "user"
        assert response.data["tokens"]["access"]
        assert response.data["tokens"]["refresh"]

        user = User.objects.get(phone_number=VALID_PHONE_E164)
        assert user.full_name == "New User"
        assert user.role == "user"

    def test_register_with_raw_phone_in_token_stores_e164(self, client):
        token = make_registration_temp_token(phone_number=VALID_PHONE_RAW)

        response = client.post(
            accounts_url("user/register/"),
            {
                "temp_token": token,
                "full_name": "Normalized User",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"]["phone_number"] == VALID_PHONE_E164
        assert User.objects.filter(phone_number=VALID_PHONE_E164).exists()

    def test_register_rejects_invalid_full_name(self, client):
        response = client.post(
            accounts_url("user/register/"),
            {
                "temp_token": make_registration_temp_token(),
                "full_name": "User123",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_with_profile_photo(self, client):
        photo = SimpleUploadedFile(
            "profile.png",
            MINIMAL_PNG,
            content_type="image/png",
        )
        response = client.post(
            accounts_url("user/register/"),
            {
                "temp_token": make_registration_temp_token(
                    phone_number="+919876543230"
                ),
                "full_name": "Photo User",
                "profile_photo": photo,
            },
            format="multipart",
        )

        assert response.status_code == status.HTTP_201_CREATED
        user = User.objects.get(phone_number="+919876543230")
        assert user.profile_photo


@pytest.mark.django_db
class TestPorterRegisterAPI:
    def test_porter_register_sets_role(self, client):
        token = make_registration_temp_token(phone_number="+919876543231")

        response = client.post(
            accounts_url("porter/register/"),
            {
                "temp_token": token,
                "full_name": "New Porter",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"]["role"] == "porter"
        user = User.objects.get(phone_number="+919876543231")
        assert user.role == "porter"


@pytest.mark.django_db
class TestPublicTokenRefreshAPI:
    def test_refresh_returns_new_access_token(self, client, existing_user):
        refresh = RefreshToken.for_user(existing_user)

        response = client.post(
            accounts_url("token/refresh/"),
            {"refresh": str(refresh)},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_refresh_invalid_token(self, client):
        response = client.post(
            accounts_url("token/refresh/"),
            {"refresh": "invalid-refresh-token"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestAuthFlowIntegration:
    """End-to-end: OTP verify (new) → register → token refresh."""

    def test_full_new_user_onboarding(self, client, mock_twilio_send):
        send_response = client.post(
            accounts_url("otp/send/"),
            {"phone_number": VALID_PHONE_RAW},
            format="json",
        )
        assert send_response.status_code == status.HTTP_200_OK

        otp = OTP.objects.filter(phone_number=VALID_PHONE_E164).latest("created_at")
        verify_response = client.post(
            accounts_url("user/otp/verify/"),
            {"phone_number": VALID_PHONE_RAW, "code": otp.code},
            format="json",
        )
        assert verify_response.status_code == status.HTTP_200_OK
        assert verify_response.data["user_status"] == "NEW"

        register_response = client.post(
            accounts_url("user/register/"),
            {
                "temp_token": verify_response.data["temp_token"],
                "full_name": "Flow User",
                "email": "flow@example.com",
            },
            format="json",
        )
        assert register_response.status_code == status.HTTP_201_CREATED

        refresh_response = client.post(
            accounts_url("token/refresh/"),
            {"refresh": register_response.data["tokens"]["refresh"]},
            format="json",
        )
        assert refresh_response.status_code == status.HTTP_200_OK
        assert refresh_response.data["access"]

    def test_existing_user_login_via_otp(self, client):
        user = create_user(phone_number="+919876543240", full_name="Returning User")
        create_otp_record(phone_number="+919876543240")

        response = client.post(
            accounts_url("user/otp/verify/"),
            {"phone_number": "9876543240", "code": VALID_OTP_CODE},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["user_status"] == "EXISTING"
        assert response.data["user"]["full_name"] == user.full_name
