from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import User, OTP, Language

# Register your models here.

class MyUser(UserAdmin, ModelAdmin):
    list_display = ("full_name", "phone_number", "email", "created_at", "is_active", "is_staff", "is_superuser") # to display in form row/column in admin panel
    list_display_links = ("full_name", "email")# to display that not only email but also both name should be clickable in home admin panel
    readonly_fields = ("phone_number", "created_at", "is_active")
    ordering = ("-created_at",)

    filter_horizontal = ()
    list_filter = ("is_active", "is_staff")
    fieldsets = ()

class MyOTP(ModelAdmin):
    list_display = ("phone_number", "code", "is_used", "created_at")
    list_display_links = ("phone_number", "code")
    readonly_fields = ("purpose", "is_used", "created_at")
    ordering = ("-created_at",)

class MyLanguage(ModelAdmin):
    list_display = ("code", "name", "is_active", "is_default", "created_at")
    list_display_links = ("code", "name")
    list_filter = ("is_active", "is_default")
    readonly_fields = ("created_at",)
    ordering = ("name",)

admin.site.register(User, MyUser)
admin.site.register(OTP, MyOTP)
admin.site.register(Language, MyLanguage)