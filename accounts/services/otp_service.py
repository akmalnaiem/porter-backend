import random
from django.utils import timezone
from datetime import timedelta
from ..models import OTP
from .twilio_service import TwilioService
from rest_framework.exceptions import ValidationError
import phonenumbers


OTP_RATE_LIMIT = 3   # max OTP per window
OTP_RATE_WINDOW = 60 # seconds

def generate_otp():
    return str(random.randint(100000, 999999))


# phone formatter
def format_phone(phone_number, region="IN"):
    try:
        parsed = phonenumbers.parse(phone_number, region)

        if not phonenumbers.is_valid_number(parsed):
            raise ValidationError("Invalid phone number")

        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)

    except Exception:
        raise ValidationError("Invalid phone number format")


def check_rate_limit(phone_number):
    time_threshold = timezone.now() - timedelta(seconds=OTP_RATE_WINDOW)

    otp_count = OTP.objects.filter(
        phone_number=phone_number,
        created_at__gte=time_threshold
    ).count()

    if otp_count >= OTP_RATE_LIMIT:
        raise ValidationError({"error" : "Too many OTP request. Try again later."})


def create_otp(phone_number):

    # ✅ Format phone
    phone_number = format_phone(phone_number)

    # ✅ Rate limiting
    check_rate_limit(phone_number)

    code = generate_otp()
    expires_at = timezone.now() + timedelta(minutes=5)

    otp = OTP.objects.create(phone_number=phone_number, code=code, expires_at=expires_at)

    # ✅ Send SMS
    sms_service = TwilioService()
    message = f"Your OTP is {code}. It will expires in 5 minutes."

    sms_sid = sms_service.send_sms(phone_number, message)

    if not sms_sid:
        otp.delete()
        # Optional: you can raise exception or handle retry logic
        # print("SMS sending failed")
        raise Exception(f"SMS sending failed after retries")

    # print(f"OTP for {phone_number} ({purpose}): {code}")
    return True

def verify_otp(phone_number, code):

    # normalizing phone number here as well
    phone_number = format_phone(phone_number)
    try:
        otp = OTP.objects.filter(phone_number=phone_number, code=code, is_used=False, expires_at__gt=timezone.now()).latest("created_at")

        # Mark as used instead of delete (production safe)
        otp.is_used = True
        otp.save()

        return True
    
    except OTP.DoesNotExist:
        return False