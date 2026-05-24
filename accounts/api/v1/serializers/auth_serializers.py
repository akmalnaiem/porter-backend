from rest_framework import serializers
from accounts.models import User
from accounts.utils import format_phone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError as DRFValidationError

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
        if value:
            return value.strip().lower()

        return value
    
    def create(self, validated_data):
        phone_number = self.context["phone_number"]
        role = self.context["role"]

        try:
            phone_number = format_phone(phone_number)
        except DRFValidationError:
            raise serializers.ValidationError(
                {"phone_number": ["Invalid phone number in registration temp token."]}
            )

        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                {"phone_number": ["An account with this phone number already exists."]}
            )

        if not phone_number:
            raise serializers.ValidationError({
                "phone_number": "Phone number not found"
            })

        if role not in ["user", "porter"]:
            raise serializers.ValidationError({
                "role": "Invalid role"
            })

        user = User.objects.create(
            phone_number = phone_number,
            full_name = validated_data["full_name"],
            email = validated_data.get("email"),
            profile_photo = validated_data.get("profile_photo"),
            role = role
        )

        refresh = RefreshToken.for_user(user)

        return {
            "user" : user,
            "access" : str(refresh.access_token),
            "refresh" : str(refresh)
        }
