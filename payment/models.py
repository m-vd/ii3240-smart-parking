import uuid
from django.db import models
from user.models import User
from ticketing.models import Ticket

# Create your models here.

class Payment(models.Model):
    paymentID   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    userID      = models.ForeignKey(User,on_delete=models.CASCADE)
    ticketID    = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    paymentTime = models.DateTimeField(auto_now_add=True)
    duration    = models.PositiveIntegerField()
    amount      = models.PositiveIntegerField()
