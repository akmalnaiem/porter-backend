from rest_framework import serializers
from accounts.services.otp_service import create_otp, verify_otp
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
import jwt
import datetime
from django.conf import settings


class SendOTPSerializer(serializers.Serializer):
    # identifier = serializers.CharField()
    phone_number = serializers.CharField()

    def create(self, validated_data):
        phone = validated_data["phone_number"]
        create_otp(phone, purpose="login")
        return validated_data
    

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code  = serializers.CharField()
    purpose = serializers.ChoiceField(choices=["login"])

    def validate(self, data):
        phone = data["phone_number"]
        
        if not verify_otp(phone, data["code"], "login"):
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
                "is_new_user" : True,
                "temp_token" : token
            }
        
        # ✅ Existing User
        refresh = RefreshToken.for_user(user)

        return {
            "is_new_user" : False,
            "access" : str(refresh.access_token),
            "refresh" : str(refresh),
            "user" : user
        }
