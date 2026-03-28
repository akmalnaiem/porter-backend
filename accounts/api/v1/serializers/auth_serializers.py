from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from accounts.utils import token_generator

# Registration Serializer-
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "profile_photo",
        ]
    
    def create(self, validated_data):
        phone_number = self.context["phone_number"]

        user = User.objects.create(
            phone_number = phone_number,
            full_name = validated_data["full_name"],
            email = validated_data.get("email"),
            profile_photo = validated_data.get("profile_photo")
        )

        refresh = RefreshToken.for_user(user)

        return {
            "user" : user,
            "access" : str(refresh.access_token),
            "refresh" : str(refresh)
        }
