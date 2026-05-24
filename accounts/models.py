import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("user", "User"),
        ("porter", "Porter"),
        ("admin", "Admin"),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    full_name = models.CharField(
        max_length=70,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex=r'^[A-Za-z ]+$',
                message = "Name should contain only letters and spaces."
            )
        ]
    )

    phone_number = models.CharField(
        max_length=16,
        unique=True,
        validators=[
            MinLengthValidator(10),
            RegexValidator(
                regex=r'^\+?\d{10,15}$'
            )
        ]
    )

    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        max_length=254
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, db_index=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def validate_image(file):
        # Size check (5MB)
        if file.size > 5 * 1024 * 1024:
            raise ValidationError("Image size should not exceed 5MB.")

        # Extension check
        valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
        ext = file.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            raise ValidationError("Only JPG, JPEG, PNG, WEBP allowed.")

    profile_photo = models.ImageField(
        upload_to="profile_photos/",
        blank=True,
        null=True,
        validators=[validate_image]
        )

    def __str__(self):
        return self.full_name


class OTP(models.Model):
    # PURPOSE_CHOICES = (
    #     ("login", "Login"),
    #     ("reset_password", "Reset Password"),
    # )
    phone_number = models.CharField(max_length=15 ,db_index=True)
    code = models.CharField(max_length=6)
    # purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default="login")                    # login, forgot_password
    purpose = models.CharField(max_length=20, default="login") 
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["phone_number", "code"])
        ]

    def __str__(self):
        return f"{self.phone_number} - {self.code}"
