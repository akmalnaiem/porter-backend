from rest_framework import serializers
from accounts.services.otp_service import create_otp, verify_otp
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from accounts.utils import token_generator


class SendOTPSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    purpose = serializers.ChoiceField(choices=["login", "reset_password"])

    def validate(self, data):
        identifier = data["identifier"]

        # Try finding user by email or phone_number
        user = User.objects.filter(phone_number=identifier).first() or User.objects.filter(email=identifier).first()

        if not user:
            raise serializers.ValidationError("User not found")
        
        data["user"] = user
        return data

    def create(self, validated_data):
        user = validated_data["user"]
        create_otp(
            user.phone_number,             # Always send OTP to phone
            validated_data["purpose"]
            )
        return validated_data
    

class VerifyOTPSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    code  = serializers.CharField()
    purpose = serializers.ChoiceField(choices=["login", "reset_password"])

    def validate(self, data):
        identifier = data["identifier"]

        user = User.objects.filter(phone_number=identifier).first() or User.objects.filter(email=identifier).first()

        if not user:
            raise serializers.ValidationError("User not found")
        
        if not verify_otp(user.phone_number, data["code"], data["purpose"]):
            raise serializers.ValidationError("Invalid or expired OTP")
        
        # LOGIN Flow
        if data["purpose"] == "login":
            refresh = RefreshToken.for_user(user)

            data["user"] = user
            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

        # Reset Password
        if data["purpose"] == "reset_password":
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = token_generator.make_token(user)

            data["uid"] = uid
            data["reset_token"] = token

        return data
