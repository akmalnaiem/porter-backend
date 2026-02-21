import random
from django.utils import timezone
from datetime import timedelta
from ..models import OTP
from .twilio_service import TwilioService

def generate_otp():
    return str(random.randint(100000, 999999))

def create_otp(phone_number, purpose):
    code = generate_otp()
    expires_at = timezone.now() + timedelta(minutes=5)

    OTP.objects.create(phone_number=phone_number, code=code, purpose=purpose, expires_at=expires_at)

    # Send SMS
    sms_service = TwilioService()
    message = f"Your OTP for {purpose} is {code}. It will expires in 5 minutes."

    sms_sid = sms_service.send_sms(phone_number, message)

    if not sms_sid:
        # Optional: you can raise exception or handle retry logic
        print("SMS sending failed")

    # print(f"OTP for {phone_number} ({purpose}): {code}")
    return True

def verify_otp(phone_number, code, purpose):
    try:
        otp = OTP.objects.filter(phone_number=phone_number, code=code, purpose=purpose, is_used=False, expires_at__gt=timezone.now()).latest("created_at")

        # Mark as used instead of delete (production safe)
        otp.is_used = True
        otp.save()

        return True
    
    except OTP.DoesNotExist:
        return False