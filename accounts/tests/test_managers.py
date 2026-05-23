import pytest

from accounts.models import User


@pytest.mark.django_db
class TestCustomUserManager:
    def test_create_user_requires_phone_number(self):
        with pytest.raises(ValueError, match="Phone number is required"):
            User.objects.create_user(phone_number="")

    def test_create_user_normalizes_email(self):
        user = User.objects.create_user(
            phone_number="+919876543212",
            full_name="Email User",
            email="Test@Example.COM",
        )
        # Django's normalize_email lowercases the domain only.
        assert user.email == "Test@example.com"

    def test_create_user_sets_unusable_password(self):
        user = User.objects.create_user(
            phone_number="+919876543213",
            full_name="No Password User",
        )
        assert not user.has_usable_password()

    def test_create_superuser_requires_password(self):
        with pytest.raises(ValueError, match="Superuser must have password"):
            User.objects.create_superuser(
                phone_number="+919876543214",
                full_name="Admin",
                password=None,
            )

    def test_create_superuser_sets_flags(self):
        user = User.objects.create_superuser(
            phone_number="+919876543215",
            full_name="Super Admin",
            email="admin@example.com",
            password="strong-test-password",
        )
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.role == "admin"
        assert user.check_password("strong-test-password")
