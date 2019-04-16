import uuid
from django.db import models

# Create your models here.

class Ticket(models.Model):
    ticketID    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    entryTime   = models.DateTimeField(auto_now_add=True)
    exitTime    = models.DateTimeField(null = True)