import uuid
from django.db import models

# Create your models here.

class Payment(models.Model):

    paymentID   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    userID      = models.CharField(max_length=30)
    ticketID    = models.CharField(max_length=30)
    paymentTime   = models.DateTimeField(auto_now_add=True)
    duration    = models.PositiveIntegerField()
    amount      = models.PositiveIntegerField()
