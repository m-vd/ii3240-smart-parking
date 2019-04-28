from django.db import models
import uuid
#from geopy.geocoders import Nominatim

class Lot(models.Model):
    lotID   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    lotName = models.CharField(max_length=30)
    updateTime   = models.DateTimeField(null = True)
    #location    = models.ForeignKey
    capacity = models.IntegerField()
    status = models.CharField(max_length=30)

