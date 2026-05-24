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
class TestUserVerifyOTPAPI:
    def test_verify_otp_new_user_returns_temp_token(self, client):
        create_otp_record()

        response = client.post(
            accounts_url("user/otp/verify/"),
            {"phone_number": VALID_PHONE_RAW, "code": VALID_OTP_CODE},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["user_status"] == "NEW"
        assert response.data["temp_token"]
        assert not User.objects.filter(phone_number=VALID_PHONE_E164).exists()

    def test_verify_otp_existing_user_with_raw_phone(self, client, existing_user):
        create_otp_record()

        response = client.post(
            accounts_url("user/otp/verify/"),
            {"phone_number": VALID_PHONE_RAW, "code": VALID_OTP_CODE},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["user_status"] == "EXISTING"
        assert "temp_token" not in response.data
        assert response.data["token"]["access"]
        assert response.data["token"]["refresh"]
        assert str(response.data["user"]["uuid"]) == str(existing_user.uuid)
        assert response.data["user"]["phone_number"] == VALID_PHONE_E164
        assert response.data["user"]["role"] == "user"

    def test_porter_account_rejected_on_user_verify(self, client):
        create_user(role="porter")
        create_otp_record()

        response = client.post(
            accounts_url("user/otp/verify/"),
            {"phone_number": VALID_PHONE_RAW, "code": VALID_OTP_CODE},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "account_type" in response.data

    def test_verify_otp_invalid_code(self, client):
        create_otp_record()

        response = client.post(
            accounts_url("user/otp/verify/"),
            {"phone_number": VALID_PHONE_RAW, "code": "000000"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid or expired OTP" in str(response.data)

    def test_verify_otp_missing_fields(self, client):
        response = client.post(accounts_url("user/otp/verify/"), {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPorterVerifyOTPAPI:
    def test_existing_porter_login(self, client):
        porter = create_user(
            phone_number="+919876543299",
            full_name="Test Porter",
            role="porter",
        )
        create_otp_record(phone_number="+919876543299")

        response = client.post(
            accounts_url("porter/otp/verify/"),
            {"phone_number": "9876543299", "code": VALID_OTP_CODE},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["user_status"] == "EXISTING"
        assert response.data["user"]["role"] == "porter"
        assert str(response.data["user"]["uuid"]) == str(porter.uuid)

    def test_user_account_rejected_on_porter_verify(self, client, existing_user):
        create_otp_record()

        response = client.post(
            accounts_url("porter/otp/verify/"),
            {"phone_number": VALID_PHONE_RAW, "code": VALID_OTP_CODE},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "account_type" in response.data
