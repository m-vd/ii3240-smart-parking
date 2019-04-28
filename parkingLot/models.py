from django.db import models
#from geopy.geocoders import Nominatim

class lot(models.Model):
    lotID    = models.CharField(max_length=30, primary_key=True, editable=False, unique=True)
    updateTime   = models.DateTimeField(null = True)
    #location    = models.CharField(max_length=30)
    capacity = models.IntegerField()
    