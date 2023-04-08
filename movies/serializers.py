from rest_framework import serializers
from .models import *

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'thumbnail', 'photo', 'description', 'movies', 'actors', 'directors']