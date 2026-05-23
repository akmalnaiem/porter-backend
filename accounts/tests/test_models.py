import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import OTP, User
from accounts.tests.helpers import VALID_PHONE_E164, create_otp_record, create_user


@pytest.mark.django_db
class TestUserModel:
    def test_str_returns_full_name(self):
        user = create_user(full_name="Jane Porter")
        assert str(user) == "Jane Porter"

    def test_uuid_is_unique_per_user(self):
        user_a = create_user(phone_number="+919876543220")
        user_b = create_user(phone_number="+919876543221")
        assert user_a.uuid != user_b.uuid

    def test_default_role_is_user(self):
        user = create_user(phone_number="+919876543222", role="user")
        assert user.role == "user"

    def test_profile_photo_rejects_invalid_extension(self):
        user = create_user(phone_number="+919876543223")
        bad_file = SimpleUploadedFile(
            "avatar.gif",
            b"fake-image-content",
            content_type="image/gif",
        )
        user.profile_photo = bad_file
        with pytest.raises(ValidationError, match="Only JPG, JPEG, PNG, WEBP"):
            user.full_clean()

    def test_profile_photo_rejects_oversized_file(self):
        user = create_user(phone_number="+919876543224")
        large_file = SimpleUploadedFile(
            "avatar.jpg",
            b"x" * (5 * 1024 * 1024 + 1),
            content_type="image/jpeg",
        )
        user.profile_photo = large_file
        with pytest.raises(ValidationError, match="5MB"):
            user.full_clean()


@pytest.mark.django_db
class TestOTPModel:
    def test_str_representation(self):
        otp = create_otp_record(code="654321")
        assert str(otp) == f"{VALID_PHONE_E164} - 654321"

    def test_defaults(self):
        otp = create_otp_record()
        assert otp.purpose == "login"
        assert otp.is_used is False
