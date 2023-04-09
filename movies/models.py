from django.db import models
from django.conf import settings

def movie_thumbnail_path(instance, filename):
    return 'files/movies/thumbnails/{0}'.format(instance.title)

def movie_poster_path(instance, filename):
    return 'files/movies/posters/{0}'.format(instance.movie.title)

def movie_actor_path(instance, filename):
    return 'files/movies/actors/{0}'.format(str(instance))

def movie_director_path(instance, filename):
    return 'files/movies/directors/{0}'.format(str(instance))

def news_thumbnail_path(instance, filename):
    return 'files/news/thumbnail/{0}/{1}'.format(instance.title,filename)

def news_photo_path(instance, filename):
    return 'files/news/photo/{0}/{1}'.format(instance.title,filename)

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
    
class Movie_meta(models.Model):
    poster = models.ImageField(upload_to=movie_poster_path)
    description = models.TextField()
    meta_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    imdb_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    publish_date = models.DateField()
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    director = models.ForeignKey('Director', on_delete=models.PROTECT)
    actors = models.ManyToManyField('Actor')

class Series_season(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    publish_date = models.DateField()
    series = models.OneToOneField(Movie, on_delete=models.CASCADE)

class Series_episode(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    publish_date = models.DateField()
    season = models.OneToOneField(Series_season, on_delete=models.CASCADE)

class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=movie_director_path)
    bio = models.TextField(null=True)
    birth_date = models.DateField()
    
    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name
    
class Director(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=movie_director_path)
    bio = models.TextField(null=True)
    birth_date = models.DateField()

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name
    
class Rating(models.Model):
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class News(models.Model):
    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=news_thumbnail_path)
    photo = models.ImageField(upload_to=news_photo_path)
    description = models.TextField()
    movies = models.ManyToManyField(Movie, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    directors = models.ManyToManyField(Director, blank=True)