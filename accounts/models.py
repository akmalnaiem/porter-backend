import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("user", "User"),
        ("porter", "Porter"),
        ("admin", "Admin"),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    full_name = models.CharField(max_length=70)

    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    profile_photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user", db_index=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.full_name
    

class OTP(models.Model):
    PURPOSE_CHOICES = (
        ("login", "Login"),
        ("reset_password", "Reset Password"),
    )
    phone_number = models.CharField(max_length=15 ,db_index=True)
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default="login")                    # login, forgot_password
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["phone_number", "code", "purpose"])
        ]

    def __str__(self):
        return f"{self.phone_number} - {self.code}"
