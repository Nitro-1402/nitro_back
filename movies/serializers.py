from rest_framework import serializers
from .models import *

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'thumbnail', 'photo', 'description', 'movies', 'actors', 'directors']

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'photo', 'bio', 'birth_date']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

class MovieSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Movie
        fields = ['id', 'title' , 'thumbnail' , 'movie_type' , 'poster' , 'description' , 'meta_rating' , 'imdb_rating' , 'publish_date' , 
                  'director' , 'actors' , 'category_set']
        
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
        fields = ['id', 'title' , 'episode_number' , 'description' , 'publish_date' , 'season']