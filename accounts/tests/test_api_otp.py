from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework import status

from accounts.models import OTP, User
from accounts.services import otp_service
from accounts.tests.helpers import (
    VALID_OTP_CODE,
    VALID_PHONE_E164,
    VALID_PHONE_RAW,
    accounts_url,
    create_otp_record,
    create_user,
)


@pytest.mark.django_db
class TestSendOTPAPI:
    def test_send_otp_success(self, client, mock_twilio_send):
        response = client.post(
            accounts_url("otp/send/"),
            {"phone_number": VALID_PHONE_RAW},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "OTP sent successfully"
        assert response.data["retry_after"] == 60
        assert OTP.objects.filter(phone_number=VALID_PHONE_E164).exists()
        mock_twilio_send.assert_called_once()

    def test_send_otp_invalid_phone(self, client):
        response = client.post(
            accounts_url("otp/send/"),
            {"phone_number": "abc"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_send_otp_rate_limited(self, client, mock_twilio_send):
        for _ in range(otp_service.OTP_RATE_LIMIT):
            OTP.objects.create(
                phone_number=VALID_PHONE_E164,
                code="111111",
                expires_at=timezone.now() + timedelta(minutes=5),
            )

        response = client.post(
            accounts_url("otp/send/"),
            {"phone_number": VALID_PHONE_RAW},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        mock_twilio_send.assert_not_called()


@pytest.mark.django_db
class TestVerifyOTPAPI:
    def test_verify_otp_new_user_returns_temp_token(self, client):
        create_otp_record()

        response = client.post(
            accounts_url("otp/verify/"),
            {"phone_number": VALID_PHONE_RAW, "code": VALID_OTP_CODE},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["user_status"] == "NEW"
        assert response.data["temp_token"]
        assert response.data["user"] is None
        assert response.data["access"] is None
        assert response.data["refresh"] is None
        assert not User.objects.filter(phone_number=VALID_PHONE_E164).exists()

    def test_verify_otp_existing_user_returns_jwt_pair(self, client, existing_user):
        create_otp_record()

        # User lookup uses the raw request value; stored numbers are E.164.
        response = client.post(
            accounts_url("otp/verify/"),
            {"phone_number": VALID_PHONE_E164, "code": VALID_OTP_CODE},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["user_status"] == "EXISTING"
        assert response.data["temp_token"] == "Null"
        assert response.data["token"]["access"]
        assert response.data["token"]["refresh"]
        assert str(response.data["user"]["uuid"]) == str(existing_user.uuid)
        assert response.data["user"]["phone_number"] == VALID_PHONE_E164

    def test_verify_otp_invalid_code(self, client):
        create_otp_record()

        response = client.post(
            accounts_url("otp/verify/"),
            {"phone_number": VALID_PHONE_RAW, "code": "000000"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid or expired OTP" in str(response.data)

    def test_verify_otp_missing_fields(self, client):
        response = client.post(accounts_url("otp/verify/"), {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
