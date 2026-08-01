from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Train

# Register your models here.

class MyTrain(ModelAdmin):
    list_display = ("id", "train_number", "train_name", "is_active")
    readonly_fields = ("id", "is_active")
    search_fields = ("train_number", "train_name")
    list_filter = ("is_active",)


admin.site.register(Train, MyTrain)