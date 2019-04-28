import uuid
from django.db import models
from user.models import User
from parkingLot.models import Lot

# Create your models here.

class Ticket(models.Model):
    ticketID    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    entryTime   = models.DateTimeField(auto_now_add=True)
    exitTime    = models.DateTimeField(null = True)
    userID      = models.ForeignKey(User,on_delete=models.CASCADE)
    location    = models.ForeignKey(Lot, on_delete=models.CASCADE)
