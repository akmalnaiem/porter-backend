from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Registration Serializer-
class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "profile_photo",
        ]

    def validate_email(self, value):
        return value.strip().lower()
    
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
