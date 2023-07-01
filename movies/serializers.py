from rest_framework import serializers
from django.db.models import Avg
from .models import *
from lists.models import *

url_prefix = "http://nitroback.pythonanywhere.com"

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'thumbnail', 'photo', 'description', 'publish_date', 'movies', 'actors', 'directors']

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'photo', 'bio', 'birth_date']

class SimpleActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name']

class SimpleDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class MovieSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Movie

        fields = ['id', 'title' , 'thumbnail' , 'movie_type' , 'poster' , 'description' , 'meta_rating' , 'imdb_rating' , 'publish_date' , 
                  'director' , 'actors' , 'category_set' , 'rating', 'country' , 'remaining_days',
                  'is_favourites', 'is_watchedList', 'is_bookmarks', 'my_rating']
                  
    director = SimpleDirectorSerializer(many=False)
    actors = SimpleActorSerializer(many=True)
    category_set = serializers.SlugRelatedField(
        many=True,
        queryset=Category.objects.all(),
        slug_field='title'
    )
        
    rating = serializers.SerializerMethodField(method_name='calculate_average_rate' , read_only= True)
    remaining_days = serializers.SerializerMethodField(method_name='calculate_days_until_publish' , read_only= True)
    thumbnail = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()
    is_favourites = serializers.SerializerMethodField()
    is_watchedList = serializers.SerializerMethodField()
    is_bookmarks = serializers.SerializerMethodField()
    my_rating = serializers.SerializerMethodField()



    def calculate_average_rate(self , movie: Movie):
        return Rating.objects.filter(movie = movie).aggregate(Avg('rating'))['rating__avg']
    
    def calculate_days_until_publish(self , movie: Movie):
        return movie.remaining_days()

    def get_thumbnail(self, movie: Movie):
        if Movie.thumbnail:
            return url_prefix + str(movie.thumbnail.url)
        return
    
    def get_poster(self, movie: Movie):
        if Movie.poster:
            return url_prefix + str(movie.poster.url)
        return
    
    def get_is_favourites(self, movie: Movie):
        if 'request' in self.context:
            me = self.context['request'].user
            if me.is_authenticated and not me.is_staff:
                return bool(Favourites.objects.filter(movie_id=movie.id).filter(profile_id=me.profile.id).exists())
            else:
                return False
        else:
            return False
    
    def get_is_watchedList(self, movie: Movie):
        if 'request' in self.context:
            me = self.context['request'].user
            if me.is_authenticated and not me.is_staff:
                return bool(Watchedlist.objects.filter(movie_id=movie.id).filter(profile_id=me.profile.id).exists())
            else:
                return False
        else:
            return False
    
    def get_is_bookmarks(self, movie: Movie):
        if 'request' in self.context:
            me = self.context['request'].user
            if me.is_authenticated and not me.is_staff:
                return bool(Bookmarks.objects.filter(movie_id=movie.id).filter(profile_id=me.profile.id).exists())
            else:
                return False
        else:
            return False
        
    def get_my_rating(self, movie: Movie):
        if 'request' in self.context:
            me = self.context['request'].user
            if me.is_authenticated and not me.is_staff:
                if Rating.objects.filter(movie_id=movie.id).filter(profile_id=me.profile.id).exists():
                    return Rating.objects.filter(movie_id=movie.id).filter(profile_id=me.profile.id).values_list('rating')[0]
        
        return 0

    
        
class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'name' , 'photo' , 'bio' , 'birth_date']

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series_season
        fields = ['id', 'title' , 'season_number' , 'series']

    series = serializers.StringRelatedField()

    def create(self, validated_data):
        movie_id = self.context['movie_id']
        return Series_season.objects.create(series_id = movie_id, **validated_data)

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series_episode
        fields = ['id' , 'title' ,'photo', 'episode_number' , 'publish_date' , 'season']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating' , 'profile' , 'movie']

