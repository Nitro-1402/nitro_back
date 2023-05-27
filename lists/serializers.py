from django.db import IntegrityError, transaction
from django.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import *
from django.db.models import Count
from movies.serializers import MovieSerializer

class AddWatchedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchedlist
        fields = ['profile', 'movie']

class RetrieveWatchedListSerializer(serializers.ModelSerializer):
    watched_list = serializers.SerializerMethodField()

    def get_watched_list(self, profile:Profile):
        return profile.watched_list.values_list('movie_id')

    class Meta:
        model = Profile
        fields = ['watched_list']

class AddFavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = ['profile', 'movie']

class RetrieveFavouritesSerializer(serializers.ModelSerializer):
    favourites = serializers.SerializerMethodField()

    def get_favourites(self, profile:Profile):
        return profile.favourites.values_list('movie_id')

    class Meta:
        model = Profile
        fields = ['favourites']

class AddBookmarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmarks
        fields = ['profile', 'movie']

class RetrieveBookmarksSerializer(serializers.ModelSerializer):
    bookmarks = serializers.SerializerMethodField()

    def get_bookmarks(self, profile:Profile):
        return profile.bookmarks.values_list('movie_id')

    class Meta:
        model = Profile
        fields = ['bookmarks']

class SeggustionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchedlist
        fields = ['movie']

    movie = serializers.SerializerMethodField(method_name='get_movie_from_id')

    def get_movie_from_id(self , movie : Movie):
        return Movie.objects.filter(id = movie.id )


