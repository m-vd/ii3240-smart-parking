import uuid
from django.db import models
from parkingLot.models import Lot

# Create your models here.

class Disaster(models.Model):
    disasterID    = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    disasterTime  = models.DateTimeField(auto_now_add=True)
    location      = models.ForeignKey(Lot,on_delete=models.CASCADE)
    status        = models.CharField(max_length=30) #resolved/unresolved
    description   = models.CharField(max_length=100)

