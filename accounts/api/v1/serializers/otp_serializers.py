import jwt
import datetime

from django.conf import settings
from django.core.validators import RegexValidator

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.services.otp_service import create_otp, verify_otp
from accounts.models import User
from accounts.utils import format_phone
from rest_framework.exceptions import ValidationError as DRFValidationError



PHONE_VALIDATOR = RegexValidator(
    regex=r'^\+?\d{10,15}$',
    message="Enter a valid phone number (10-15 digits, optional +91)"
)

ROLE_MESSAGES = {
    ("user", "porter"): (
        "This phone number is registered as a customer account. Please use the customer app to continue."
    ),

    ("porter", "user"): (
        "This phone number is registered as a porter account. Please use the porter app to continue."
    ),
}

class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        validators = [PHONE_VALIDATOR]
    )

    def validate_phone_number(self, value):
        try:
            return format_phone(value)
        except DRFValidationError as exc:
            detail = exc.detail
            message = detail[0] if isinstance(detail, list) else detail
            raise serializers.ValidationError({"phone_number": [str(message)]})

    def create(self, validated_data):
        phone = validated_data["phone_number"]
        create_otp(phone)
        return validated_data

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        validators = [PHONE_VALIDATOR]
    )

    def validate_phone_number(self, value):
        try:
            return format_phone(value)
        except DRFValidationError as exc:
            detail = exc.detail
            message = detail[0] if isinstance(detail, list) else detail
            raise serializers.ValidationError({"phone_number": [str(message)]})

    code  = serializers.CharField(
        min_length=6,
        max_length=6,
        error_messages={
            "min_length": "OTP must be 6 digits",
            "max_length": "OTP must be 6 digits"
        },
    )

    def validate(self, data):
        phone = data["phone_number"]
        code = data["code"]
        expected_role = self.context["role"]
        
        # OTP Validation
        if not verify_otp(phone, code):
            raise serializers.ValidationError({"code": ["Invalid or expired OTP."]})

        user = User.objects.filter(phone_number=phone).first()

        # ✅ New User
        if not user:
            token = jwt.encode(
                {
                    "phone_number" : phone,
                    "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
                },
                settings.SECRET_KEY,
                algorithm="HS256"
            )
            return {
                "user_status" : "NEW",
                "temp_token" : token,
                "user" : None,
                "access" : None,
                "refresh" : None
            }

        # ✅ Existing User

        # APP ROLE VALIDATION
        if user.role != expected_role:
            error_message = ROLE_MESSAGES[
                (user.role, expected_role)
            ]

            raise serializers.ValidationError({
                "account_type": [error_message]
            })

        # JWT TOKEN GENERATION
        refresh = RefreshToken.for_user(user)

        return {
            "user_status" : "EXISTING",
            "temp_token" : None,
            "user" : user,
            "access" : str(refresh.access_token),
            "refresh" : str(refresh),
        }
