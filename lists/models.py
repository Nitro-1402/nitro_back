from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
class User_list(models.Model):
    LIST_FAVORITE = 'F'
    LIST_WATCHLIST = 'W'
    LIST_CUSTOM = 'C'
    LIST_CHOICES = [
        (LIST_FAVORITE, 'Favorites'),
        (LIST_WATCHLIST, 'Watchlist'),
        (LIST_CUSTOM, 'Custom'),
    ] 
    title = models.CharField(max_length=255,default="Favorites")
    user_list_type = models.CharField(
        max_length=1, choices=LIST_CHOICES, default=LIST_FAVORITE)
    private = models.BooleanField(default=False)
    description = models.TextField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)



class List_movie(models.Model):
    user_list = models.ForeignKey(User_list, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

