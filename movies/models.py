from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator

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
    director = models.ForeignKey('Director', on_delete=models.PROTECT)
    actors = models.ManyToManyField('Actor')

    def __str__(self) -> str:
        return self.title
    

class Series_season(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    publish_date = models.DateField()
    series = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Series_episode(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    publish_date = models.DateField()
    season = models.ForeignKey(Series_season, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user + ' rated ' + self.movie + ' with rating: ' + self.rating

class News(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=news_thumbnail_path)
    photo = models.ImageField(upload_to=news_photo_path)
    description = models.TextField()
    movies = models.ManyToManyField(Movie, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    directors = models.ManyToManyField(Director, blank=True)

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movie, blank=True)
    
    def __str__(self) -> str:
        return self.title