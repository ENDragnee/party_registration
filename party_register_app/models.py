# registration/models.py
import uuid
from django.db import models


class Guest(models.Model):
    # Status choices for the guest's check-in status
    class Status(models.TextChoices):
        VALID = 'VALID', 'Valid'
        ENTERED = 'ENTERED', 'Entered'

    # Fields for the registration form
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    will_attend = models.BooleanField(default=False)

    # Internal fields for tracking
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.VALID
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

# Create your models here.
