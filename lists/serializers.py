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
        movies = Movie.objects.filter(id__in=profile.watched_list.values_list('movie_id'))
        return MovieSerializer(movies, many=True).data
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
        movies = Movie.objects.filter(id__in=profile.favourites.values_list('movie_id'))
        return MovieSerializer(movies, many=True).data

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
        movies = Movie.objects.filter(id__in=profile.bookmarks.values_list('movie_id'))
        return MovieSerializer(movies, many=True).data

    class Meta:
        model = Profile
        fields = ['bookmarks']

class SeggustionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchedlist
        fields = ['movie']

    movie = MovieSerializer()

    # def get_movie_id(self, watched_list: Watchedlist):
    #     movies = Movie.objects.filter(id= watched_list.movie_id)
    #     return Movie()

