import uuid
from django.db import models
from user.models import User


# Create your models here.

class Help(models.Model):
    helpID          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    questionTime    = models.DateTimeField(auto_now_add=True)
    answerTime      = models.DateTimeField(null = True)
    user            = models.ForeignKey(User, on_delete= models.CASCADE)
    question        = models.CharField(max_length=300)
    answer          = models.CharField(max_length=300, null=True)