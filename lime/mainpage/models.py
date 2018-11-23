from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username = models.CharField(max_length=128)
    TYPE_CHOICE = (('M', "مرد"),
                   ('F', "زن"),
                   )
    picture = models.FileField(blank=True, null=True, upload_to='lime/static/imgs')
    bio = models.CharField(max_length=1028)
    gender = models.CharField(max_length=20, choices=TYPE_CHOICE, default='M')

    def image_tag(self):
        return mark_safe("<img src='/%s' style='max-width:250px; height=auto'/>" % self.picture)
