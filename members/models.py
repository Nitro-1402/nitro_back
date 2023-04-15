from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

def profile_photo_path(instance, filename):
    return 'members/photos/{0}'.format(instance.user.username)

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self) -> str:
        return self.username

class Profile(models.Model):
    photo = models.ImageField(upload_to=profile_photo_path,blank=True , null=True)
    first_name = models.CharField(max_length=255,blank=True , null=True)
    last_name = models.CharField(max_length=255,blank=True , null=True)
    bio = models.TextField(null=True,blank=True)
    birth_date = models.DateField(blank=True , null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Follows = models.ManyToManyField('Profile')
    
    def __str__(self) -> str:
        return self.user.username
