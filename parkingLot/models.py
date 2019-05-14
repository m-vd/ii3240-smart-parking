from django.db import models
import uuid, decimal
#from geopy.geocoders import Nominatim

class Lot(models.Model):
    lotID       = models.CharField(primary_key=True, max_length=30, unique=True)
        # Motor_Sipil : Parkiran Motor Sipil
        # Motor_SR    : Parkiran Motor SR
        # Mobil_SR    : Parkiran Mobil SR
        # Mobil_Dalam
        # Motor_Dalam
    lotName     = models.CharField(max_length=30)
    updateTime  = models.DateTimeField(null = True)
    capacity    = models.IntegerField()
    status      = models.CharField(max_length=30)
    lat         = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    long        = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

