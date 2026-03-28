from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self,phone_number, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")
        
        email = extra_fields.get("email")
        if email:
            extra_fields["email"] = self.normalize_email(email)

        user = self.model(phone_number=phone_number, **extra_fields)

        user.set_unusable_password()
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if not password:
            raise ValueError("Superuser must have password")
        
        return self.create_user(phone_number, password, **extra_fields)