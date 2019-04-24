from django.db import models

# Create your models here.
class User(models.Model):
    userID      = models.CharField(max_length=30, primary_key=True)
    userName    = models.CharField(max_length=50)
    userEmail   = models.CharField()
    cardNumber  = models.CharField()
    userMoney   = models.PositiveIntegerField()