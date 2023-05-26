from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from datetime import date
from comments.models import *
from members.models import Profile
import datetime

def movie_thumbnail_path(instance, filename):
    return 'movies/thumbnails/{0}/{1}'.format(instance.title,filename)

def movie_poster_path(instance, filename):
    return 'movies/posters/{0}/{1}'.format(instance.title,filename)

def movie_actor_path(instance, filename):
    return 'movies/actors/{0}/{1}'.format(str(instance),filename)

def movie_director_path(instance, filename):
    return 'movies/directors/{0}/{1}'.format(str(instance),filename)

def news_thumbnail_path(instance, filename):
    return 'news/thumbnail/{0}/{1}'.format(instance.title,filename)

def news_photo_path(instance, filename):
    return 'news/photo/{0}/{1}'.format(instance.title,filename)

def episode_photo_path(instance, filename):
    return 'episode/photo/{0}/{1}'.format(instance.episode_number,filename)

class Movie(models.Model):
    MOVIETYPE_MOVIE = 'M'
    MOVIETYPE_SERIES = 'S'

    MOVIETYPE_CHOICES = [
        (MOVIETYPE_MOVIE, 'Movie'),
        (MOVIETYPE_SERIES, 'Series'),
    ]

    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=movie_thumbnail_path)
    movie_type = models.CharField(
        max_length=1, choices=MOVIETYPE_CHOICES, default=MOVIETYPE_MOVIE)
    poster = models.ImageField(upload_to=movie_poster_path)
    description = models.TextField()
    meta_rating = models.PositiveSmallIntegerField(null=True , blank=True , validators=[MaxValueValidator(100)])
    imdb_rating = models.PositiveSmallIntegerField(null=True , blank=True , validators=[MaxValueValidator(100)])
    publish_date = models.DateField()
    country = models.CharField(max_length=255)
    director = models.ForeignKey('Director', on_delete=models.PROTECT)
    actors = models.ManyToManyField('Actor')
    comments = GenericRelation(Comment)

    def __str__(self) -> str:
        return self.title
    
    def remaining_days(self):
        remainday = (self.publish_date - datetime.datetime.now().date()).days
        if remainday <= 0:
            remainday = 0
        return remainday
    

class Series_season(models.Model):
    title = models.CharField(max_length=255)
    season_number = models.PositiveBigIntegerField()
    series = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.series) + ' season ' + str(self.season_number)

class Series_episode(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=episode_photo_path, null=True)
    episode_number = models.PositiveBigIntegerField()
    publish_date = models.DateField()
    season = models.ForeignKey(Series_season, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.season) + ' episode ' + str(self.episode_number)

class Actor(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=movie_actor_path)
    bio = models.TextField(null=True)
    birth_date = models.DateField()
    
    def __str__(self) -> str:
        return self.name
    
class Director(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=movie_director_path)
    bio = models.TextField(null=True)
    birth_date = models.DateField()

    def __str__(self) -> str:
        return self.name
    
class Rating(models.Model):
    rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profile + ' rated ' + self.movie + ' with rating: ' + self.rating

class News(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=news_thumbnail_path)
    photo = models.ImageField(upload_to=news_photo_path)
    description = models.TextField()
    publish_date = models.DateField(default=date.today, blank=True)
    movies = models.ManyToManyField(Movie, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    directors = models.ManyToManyField(Director, blank=True)
    comments = GenericRelation(Comment)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movie, blank=True , related_name='category_set')
    
    def __str__(self) -> str:
        return self.title