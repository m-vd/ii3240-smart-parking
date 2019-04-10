from django.db import models

# Create your models here.
class ParkRecord(models.Model):
    parkID = models.CharField(max_length=200)
    userID = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, default="asd")
    checkInTime = models.DateTimeField(auto_now_add=True)
    checkOutTime = models.DateTimeField(blank=True)
    status = models.CharField(max_length=200, blank=True)


