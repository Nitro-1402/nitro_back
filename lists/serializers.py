from django.db import IntegrityError, transaction
from django.conf import settings
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import *

class AddWatchedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchedlist
        fields = ['profile', 'movie']

class RetrieveWatchedListSerializer(serializers.ModelSerializer):
    watched_list = serializers.SerializerMethodField()

    def get_watched_list(self, profile:Profile):
        return profile.watched_list.movie.id

    class Meta:
        model = Profile
        fields = ['watched_list']
