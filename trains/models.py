from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Train(models.Model):
    train_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{5,6}$',
                message='Train number must be 5 or 6 digits.'
            )
        ],
        verbose_name='Train Number'
    )

    train_name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name='Train Name'
    )

    is_active = models.BooleanField(default=True, verbose_name='Is Active')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering= ['train_number']

    def __str__(self):
        return f"{self.train_number} - {self.train_name}"