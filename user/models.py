from django.db import models

# Create your models here.
class User(models.Model):
    userID      = models.CharField(max_length=30, primary_key=True)
    userName    = models.CharField(max_length=50)
    userEmail   = models.EmailField(max_length=50)
    userPhone   = models.CharField(max_length=13)
    userType    = models.SmallIntegerField()
        # 1 - mahasiswa
        # 2 - dosen
        # 3 - staff teknis
        # 4 - staff akademik kampus
        # 5 - tamu
        # 6 - dekan
        # 7 - kaprodi
        # 8 - admin
    cardNumber  = models.CharField(max_length=50)
    userBalance = models.PositiveIntegerField()