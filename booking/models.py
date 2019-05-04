import uuid
from django.db import models
from user.models import User
from parkingLot.models import Lot

# Create your models here.

class Booking(models.Model):

    bookingID   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    bookingTime = models.DateTimeField(null=True)
    location    = models.ForeignKey(Lot, on_delete=models.CASCADE)
    status      = models.CharField(max_length=30)
