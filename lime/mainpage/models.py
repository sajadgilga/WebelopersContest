from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=128)
    TYPE_CHOICE = (('M', "مرد"),
                   ('F', "زن"),
                   )
    picture = models.FileField(blank=True, null=True, upload_to='static/imgs')
    bio = models.CharField(max_length=1028)
    gender = models.CharField(max_length=20, choices=TYPE_CHOICE, default='M')