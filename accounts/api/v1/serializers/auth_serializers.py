from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from accounts.utils import token_generator

# Registration Serializer-
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "uuid",
            "full_name",
            "phone_number",
            "email",
            "profile_photo",
            "password",
            "confirm_password",
        ]

        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data)

# Login Serializer-
class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        identifier = data["identifier"]
        password = data["password"]

        user = User.objects.filter(phone_number=identifier).first() or User.objects.filter(email=identifier).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")
        
        data["user"] = user

        return data
    

# Reset_Password Serializer-
class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    reset_token = serializers.CharField()
    new_password = serializers.CharField(min_length=6)
    confirm_password = serializers.CharField(min_length=6)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")

        try:
            user_id = force_str(urlsafe_base64_decode(data["uid"]))
            user = User.objects.get(id=user_id)
        except:
            raise serializers.ValidationError("Invalid user")

        if not token_generator.check_token(user, data["reset_token"]):
            raise serializers.ValidationError("Invalid or expired reset token")

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
