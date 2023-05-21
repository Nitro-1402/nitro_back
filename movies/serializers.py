from rest_framework import serializers
from django.db.models import Avg
from .models import *

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'thumbnail', 'photo', 'description', 'publish_date', 'movies', 'actors', 'directors']

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'photo', 'bio', 'birth_date']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class MovieSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Movie

        fields = ['id', 'title' , 'thumbnail' , 'movie_type' , 'poster' , 'description' , 'meta_rating' , 'imdb_rating' , 'publish_date' , 
                  'director' , 'actors' , 'category_set' , 'rating', 'country']
        
    rating = serializers.SerializerMethodField(method_name='calculate_average_rate' , read_only= True)

    def calculate_average_rate(self , movie : Movie):
        return Rating.objects.filter(movie = movie).aggregate(Avg('rating'))['rating__avg']

        
class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name' , 'photo' , 'bio' , 'birth_date']

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series_season
        fields = ['id', 'title' , 'season_number' , 'description' , 'publish_date' , 'series']

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series_episode
        fields = ['id' , 'title' , 'episode_number' , 'description' , 'publish_date' , 'season']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating' , 'profile' , 'movie']

