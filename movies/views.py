from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

class NewsViewSet(ModelViewSet):
    queryset = News.objects.prefetch_related(
        'movies').prefetch_related('actors').prefetch_related('directors').all()
    serializer_class = NewsSerializer

class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.select_related('director').prefetch_related('actors').prefetch_related('category_set').all()
    serializer_class = MovieSerializer

class DirctorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class SeasonViewSet(ModelViewSet):
    queryset = Series_season.objects.select_related('series').all()
    serializer_class = SeasonSerializer

class EpisodeViewSet(ModelViewSet):
    queryset = Series_episode.objects.select_related('season').all()
    serializer_class = EpisodeSerializer