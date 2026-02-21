from twilio.rest import Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TwilioService:
    def __init__(self):
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        self.from_number = settings.TWILIO_PHONE_NUMBER

    def send_sms(self, phone_number, message):
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=f"+91{phone_number}"
            )
            return message.sid
        
        except Exception as e:
            logger.error(f"Twilio SMS failed: {str(e)}")
            return None