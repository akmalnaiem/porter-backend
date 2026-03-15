from django.db import models

# Create your models here.

class Station(models.Model):
    stnCode = models.CharField(max_length=10, unique=True, blank=False)
    stnName = models.CharField(max_length=120, blank=False)
    stnCity = models.CharField(max_length=120, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["stnName"]
        indexes = [
            models.Index(fields=["stnCode"]),
            models.Index(fields=["stnName"]),
            models.Index(fields=["stnCity"]),
        ]


    def __str__(self):
        return f"{self.stnName} ({self.stnCode})"
