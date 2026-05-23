from datetime import timedelta
from unittest.mock import patch

import pytest
from django.test import override_settings
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from accounts.models import OTP
from accounts.services import otp_service
from accounts.tests.helpers import VALID_PHONE_E164, VALID_PHONE_RAW, VALID_OTP_CODE


@pytest.mark.django_db
class TestFormatPhone:
    def test_formats_indian_number_to_e164(self):
        assert otp_service.format_phone(VALID_PHONE_RAW) == VALID_PHONE_E164

    def test_accepts_e164_input(self):
        assert otp_service.format_phone(VALID_PHONE_E164) == VALID_PHONE_E164

    def test_rejects_invalid_number(self):
        with pytest.raises(ValidationError, match="Invalid phone number"):
            otp_service.format_phone("123")


@pytest.mark.django_db
class TestGenerateOtp:
    def test_generates_six_digit_code(self):
        code = otp_service.generate_otp()
        assert len(code) == 6
        assert code.isdigit()


@pytest.mark.django_db
class TestCheckRateLimit:
    def test_allows_requests_under_limit(self):
        for _ in range(otp_service.OTP_RATE_LIMIT - 1):
            OTP.objects.create(
                phone_number=VALID_PHONE_E164,
                code="111111",
                expires_at=timezone.now() + timedelta(minutes=5),
            )
        otp_service.check_rate_limit(VALID_PHONE_E164)

    def test_blocks_when_limit_exceeded(self):
        for _ in range(otp_service.OTP_RATE_LIMIT):
            OTP.objects.create(
                phone_number=VALID_PHONE_E164,
                code="222222",
                expires_at=timezone.now() + timedelta(minutes=5),
            )
        with pytest.raises(ValidationError, match="Too many OTP"):
            otp_service.check_rate_limit(VALID_PHONE_E164)


@pytest.mark.django_db
class TestCreateOtp:
    def test_creates_otp_and_sends_sms(self, mock_twilio_send):
        result = otp_service.create_otp(VALID_PHONE_RAW)

        assert result is True
        assert OTP.objects.filter(phone_number=VALID_PHONE_E164).exists()
        mock_twilio_send.assert_called_once()
        call_args = mock_twilio_send.call_args[0]
        assert call_args[0] == VALID_PHONE_E164
        assert "Your OTP is" in call_args[1]

    def test_deletes_otp_when_sms_fails(self, mock_twilio_send_failure):
        with pytest.raises(ValidationError, match="Failed to send OTP"):
            otp_service.create_otp(VALID_PHONE_RAW)

        assert not OTP.objects.filter(phone_number=VALID_PHONE_E164).exists()

    @override_settings(OTP_BYPASS_NUMBERS=[VALID_PHONE_E164])
    def test_bypass_number_skips_twilio(self):
        with patch("accounts.services.otp_service.TwilioService.send_sms") as send_sms:
            otp_service.create_otp(VALID_PHONE_RAW)

        send_sms.assert_not_called()
        assert OTP.objects.filter(phone_number=VALID_PHONE_E164).exists()


@pytest.mark.django_db
class TestVerifyOtp:
    def test_valid_otp_is_marked_used(self):
        otp = OTP.objects.create(
            phone_number=VALID_PHONE_E164,
            code=VALID_OTP_CODE,
            expires_at=timezone.now() + timedelta(minutes=5),
        )

        assert otp_service.verify_otp(VALID_PHONE_RAW, VALID_OTP_CODE) is True

        otp.refresh_from_db()
        assert otp.is_used is True

    def test_wrong_code_returns_false(self):
        OTP.objects.create(
            phone_number=VALID_PHONE_E164,
            code=VALID_OTP_CODE,
            expires_at=timezone.now() + timedelta(minutes=5),
        )
        assert otp_service.verify_otp(VALID_PHONE_RAW, "000000") is False

    def test_expired_otp_returns_false(self):
        OTP.objects.create(
            phone_number=VALID_PHONE_E164,
            code=VALID_OTP_CODE,
            expires_at=timezone.now() - timedelta(minutes=1),
        )
        assert otp_service.verify_otp(VALID_PHONE_RAW, VALID_OTP_CODE) is False

    def test_already_used_otp_returns_false(self):
        OTP.objects.create(
            phone_number=VALID_PHONE_E164,
            code=VALID_OTP_CODE,
            expires_at=timezone.now() + timedelta(minutes=5),
            is_used=True,
        )
        assert otp_service.verify_otp(VALID_PHONE_RAW, VALID_OTP_CODE) is False

    def test_uses_latest_valid_otp_when_multiple_exist(self):
        OTP.objects.create(
            phone_number=VALID_PHONE_E164,
            code="111111",
            expires_at=timezone.now() + timedelta(minutes=5),
        )
        latest = OTP.objects.create(
            phone_number=VALID_PHONE_E164,
            code=VALID_OTP_CODE,
            expires_at=timezone.now() + timedelta(minutes=5),
        )

        assert otp_service.verify_otp(VALID_PHONE_RAW, VALID_OTP_CODE) is True
        latest.refresh_from_db()
        assert latest.is_used is True
