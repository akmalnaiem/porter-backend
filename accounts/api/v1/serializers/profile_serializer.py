from rest_framework import serializers
from django.db import transaction

from accounts.models import User, Language

# Profile Update Serializer

class ProfileUpdateSerializer(serializers.ModelSerializer):

    language = serializers.PrimaryKeyRelatedField(
        queryset = Language.objects.filter(is_active=True),
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "profile_photo",
            "language",
            "gender",
            "city",
        ]

        extra_kwargs = {
            "full_name": {
                "required": False,
            },
            "email": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
            "profile_photo": {
                "required": False,
                "allow_null": True,
            },
            "gender": {
                "required": False,
                "allow_null": True,
            },
            "city": {
                "required": False,
                "allow_null": True,
                "allow_blank": True,
            },
        }

    # Email Validation
    def validate_email(self, value):
        if not value:
            return None

        value = value.strip().lower()

        existing_user = User.objects.filter(email=value).exclude(pk=self.instance.pk).exists()

        if existing_user:
            raise serializers.ValidationError(
                "This email is already in use."
            )    
        return value

    # Full Name Validation
    def validate_full_name(self, value):

        return value.strip()

    # City Validation
    def validate_city(self, value):

        user = self.instance

        # Porter cannot update city
        if user.role == "porter":
            raise serializers.ValidationError(
                "City can only be updated by user."
            )

        if value:
            value = value.strip()

        return value

    # Object Level Validation
    def validate(self, attrs):
        user = self.instance
# safety check
        # safety check
        if user.role == "porter" and "city" in attrs:
            raise serializers.ValidationError({
                "city": [
                    "City is not applicable for porter accounts."
                ]
            })

        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):

        instance.full_name = validated_data.get("full_name", instance.full_name)

        instance.email = validated_data.get("email", instance.email)

        instance.profile_photo = validated_data.get("profile_photo", instance.profile_photo)

        instance.language = validated_data.get("language", instance.language)

        instance.gender = validated_data.get("gender", instance.gender)

        # Traveller Only
        if instance.role == "user":
            instance.city = validated_data.get("city", instance.city)

        instance.save()

        return instance
