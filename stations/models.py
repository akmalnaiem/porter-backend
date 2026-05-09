from django.db import models

# Create your models here.

class Station(models.Model):
    stn_code = models.CharField(max_length=10, unique=True, blank=False)
    stn_name = models.CharField(max_length=120, blank=False)
    stn_city = models.CharField(max_length=120, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["stn_name"]
        indexes = [
            models.Index(fields=["stn_code"]),
            models.Index(fields=["stn_name"]),
            models.Index(fields=["stn_city"]),
        ]


    def __str__(self):
        return f"{self.stn_name} ({self.stn_code})"
