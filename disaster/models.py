import uuid
from django.db import models
from parkingLot.models import lot

# Create your models here.

class Disaster(models.Model):

    disasterID   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    disasterTime   = models.DateTimeField(auto_now_add=True)
    location      = models.ManyToManyField(lot,blank=True)
    status        = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
