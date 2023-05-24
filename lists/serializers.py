from django.db import IntegrityError, transaction
from django.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import *
from movies.serializers import MovieSerializer

class AddWatchedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchedlist
        fields = ['profile', 'movie']

class RetrieveWatchedListSerializer(serializers.ModelSerializer):
    watched_list = serializers.SerializerMethodField()

    def get_watched_list(self, profile:Profile):
        movies = profile.watched_list.values('movie_id')
        return MovieSerializer(movies)

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