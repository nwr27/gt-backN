from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    rfid_user = models.CharField(max_length=100, unique=True, null=True, blank=True)
    telegram = models.CharField(max_length=100, unique=True, null=True, blank=True)
    no_hp = models.CharField(max_length=20, null=True, blank=True)
    nik = models.CharField(max_length=50, unique=True, null=True, blank=True)
    bagian = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Profile"
    
class Garment(models.Model):
    id_garment = models.AutoField(primary_key=True)
    rfid_garment = models.CharField(max_length=36)
    item = models.CharField(max_length=30)
    buyer = models.CharField(max_length=30)
    style = models.CharField(max_length=30)
    wo = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    size = models.CharField(max_length=30)

    output = models.IntegerField(null=True, blank=True)
    output_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "garment"
        managed = False   # important, because table already exists

    def __str__(self):
        return f"{self.rfid_garment} - {self.item}"