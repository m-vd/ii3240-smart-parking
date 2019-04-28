import uuid
from django.db import models

# Create your models here.

class Booking(models.Model):

    bookingID   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    userID      = models.CharField(max_length=30)
    bookingTime   = models.DateTimeField(auto_now_add=True)
    location      = models.CharField(max_length=30)
    status        = models.CharField(max_length=30)
