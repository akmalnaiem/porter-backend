from django.apps import AppConfig
from django.contrib.auth import get_user_model


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):

        User = get_user_model()

        try:
            if not User.objects.filter(email="akmalnaiem25@gmail.com").exists():
                User.objects.create_superuser(
                    email="akmalnaiem25@gmail.com",
                    phone_number="7828807574",
                    password="zzpp57t83DaBms"
                )
        except Exception:
            pass