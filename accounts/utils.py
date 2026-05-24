import phonenumbers
from rest_framework.exceptions import ValidationError


def format_phone(phone_number: str, region: str = "IN") -> str:
    """Normalize phone numbers to E.164 (e.g. +919876543210)."""
    try:
        parsed = phonenumbers.parse(phone_number, region)

        if not phonenumbers.is_valid_number(parsed):
            raise ValidationError("Invalid phone number")

        return phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.E164
        )

    except ValidationError:
        raise
    except Exception:
        raise ValidationError("Invalid phone number format")
