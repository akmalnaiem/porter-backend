import datetime
import uuid

import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.models import OTP, User

ACCOUNTS_API_PREFIX = "/api/v1/accounts/"
VALID_PHONE_RAW = "9876543210"
VALID_PHONE_E164 = "+919876543210"
VALID_OTP_CODE = "123456"


def accounts_url(path: str) -> str:
    return f"{ACCOUNTS_API_PREFIX}{path.lstrip('/')}"


def create_user(
    *,
    phone_number: str = VALID_PHONE_E164,
    full_name: str = "Test User",
    email: str | None = None,
    role: str = "user",
) -> User:
    if email is None:
        email = f"user_{uuid.uuid4().hex[:10]}@example.com"
    return User.objects.create_user(
        phone_number=phone_number,
        full_name=full_name,
        email=email,
        role=role,
    )


def create_otp_record(
    *,
    phone_number: str = VALID_PHONE_E164,
    code: str = VALID_OTP_CODE,
    minutes_valid: int = 5,
    is_used: bool = False,
) -> OTP:
    return OTP.objects.create(
        phone_number=phone_number,
        code=code,
        expires_at=timezone.now() + datetime.timedelta(minutes=minutes_valid),
        is_used=is_used,
    )


def make_registration_temp_token(
    phone_number: str = VALID_PHONE_E164,
    *,
    expired: bool = False,
    invalid: bool = False,
) -> str:
    if invalid:
        return "not-a-valid-jwt"

    if expired:
        exp = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
    else:
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=20)

    return jwt.encode(
        {"phone_number": phone_number, "exp": exp},
        settings.SECRET_KEY,
        algorithm="HS256",
    )


def api_client() -> APIClient:
    return APIClient()
