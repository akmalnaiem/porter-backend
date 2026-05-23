"""
Minimal overrides for running the test suite locally and in CI.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

os.environ.setdefault("SECRET_KEY", "django-insecure-pytest-only-change-in-ci")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("DB_NAME", "test_db")
os.environ.setdefault("DB_USER", "test_user")
os.environ.setdefault("DB_PASSWORD", "test_password")
os.environ.setdefault("DB_HOST", "127.0.0.1")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("TWILIO_ACCOUNT_SID", "AC00000000000000000000000000000000")
os.environ.setdefault("TWILIO_AUTH_TOKEN", "pytest-twilio-auth-token")
os.environ.setdefault("TWILIO_PHONE_NUMBER", "+15555550100")
os.environ.setdefault("OTP_BYPASS_NUMBERS", "")

from porter_connect.settings import *  # noqa: E402, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    }
}

SECRET_KEY = "django-insecure-pytest-only-change-in-ci"
OTP_BYPASS_NUMBERS = []
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
