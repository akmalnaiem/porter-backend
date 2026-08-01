from rest_framework import serializers
from accounts.models import User, Language
from accounts.utils import format_phone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError as DRFValidationError

# Registration Serializer-
class RegisterSerializer(serializers.ModelSerializer):

    language = serializers.PrimaryKeyRelatedField(
        queryset = Language.objects.filter(is_active=True),
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "full_name",
            "language",
            "email",
            "profile_photo",
        ]

    # -------------------------------
    # Email Validation
    # -------------------------------
    def validate_email(self, value):
        if value:
            return value.strip().lower()

        return value

    # -------------------------------
    # Registration Logic
    # -------------------------------
    def create(self, validated_data):
        phone_number = self.context["phone_number"]
        role = self.context["role"]

        # Validate phone number received from temp token
        try:
            phone_number = format_phone(phone_number)
        except DRFValidationError:
            raise serializers.ValidationError(
                {"phone_number": ["Invalid phone number in registration temp token."]}
            )

        # Prevent duplicate registration
        if User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                {"phone_number": ["An account with this phone number already exists."]}
            )

        if not phone_number:
            raise serializers.ValidationError({
                "phone_number": "Phone number not found"
            })

        # Validate role
        if role not in ["user", "porter"]:
            raise serializers.ValidationError({
                "role": "Invalid role"
            })

        language = validated_data.get("language") or Language.get_default()

        # Create User
        user = User.objects.create(
            phone_number = phone_number,
            full_name = validated_data["full_name"],
            language = language,
            email = validated_data.get("email"),
            profile_photo = validated_data.get("profile_photo"),
            role = role
        )

        # Generate JWT Tokens
        refresh = RefreshToken.for_user(user)

        return {
            "user" : user,
            "access" : str(refresh.access_token),
            "refresh" : str(refresh)
        }
