from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(unique=True)

def member_photo_path(instance, filename):
    return 'members/photos/{0}'.format(instance.user.username)

class Member(models.Model):
    photo = models.ImageField(upload_to=member_photo_path, null=True)
    phone = models.CharField(max_length=255)
    bio = models.TextField(null=True)
    birth_date = models.DateField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

