from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from movies.models import Movie
from members.models import Profile

class Watchedlist(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='watched_list')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)





# class List_movie(models.Model):
#     user_list = models.ForeignKey(User_list, on_delete=models.CASCADE)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

