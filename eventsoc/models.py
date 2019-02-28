from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# These field types will probably need changing
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length = 30)
    email = models.CharField(max_length = 30)
    logo = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
