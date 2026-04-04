from twilio.rest import Client
from django.conf import settings
import logging, time

logger = logging.getLogger(__name__)

class TwilioService:
    def __init__(self):
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        self.from_number = settings.TWILIO_PHONE_NUMBER

    def send_sms(self, phone_number, message, retries=3):
        for attempt in range(retries):
            try:
                msg = self.client.messages.create(
                    body=message,
                    from_=self.from_number,
                    to=phone_number             # already formate in otp_service
                )
                return msg.sid

            except Exception as e:
                logger.error(f"Twilio attempt {attempt+1} failed: {str(e)}")

                # last attempt → fail
                if attempt == retries - 1:
                    return None

                # small delay before retry (important)
                time.sleep(1)