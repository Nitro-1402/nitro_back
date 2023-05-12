from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from movies.models import Movie

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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.user.username
    
class UserFollow(models.Model):
    follower_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followings')
    following_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    body = models.TextField()
    is_premium = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Subscribe(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscribers')
    subscriber_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscribed_to')
    created_at = models.DateTimeField(auto_now_add=True)