from rest_framework import serializers
from accounts.services.otp_service import create_otp, verify_otp
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
import datetime
from django.conf import settings
from django.core.validators import RegexValidator


class SendOTPSerializer(serializers.Serializer):
    # identifier = serializers.CharField()
    phone_number = serializers.CharField(
    validators=[
        RegexValidator(
            regex=r'^\+?\d{10,15}$',
            message="Enter a valid phone number (10-15 digits, optional +91)"
            )
        ]
    )

    def create(self, validated_data):
        phone = validated_data["phone_number"]
        create_otp(phone)
        return validated_data
    

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code  = serializers.CharField()

    def validate(self, data):
        phone = data["phone_number"]
        
        if not verify_otp(phone, data["code"]):
            raise serializers.ValidationError("Invalid or expired OTP")
        
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
        refresh = RefreshToken.for_user(user)

        return {
            "user_status" : "EXISTING",
            "temp_token" : "Null",
            "access" : str(refresh.access_token),
            "refresh" : str(refresh),
            "user" : user
        }
