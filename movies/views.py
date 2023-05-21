from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import *
from .models import *
from .serializers import *
from .pagination import *
from .permissions import *

class NewsViewSet(ModelViewSet):
    queryset = News.objects.prefetch_related(
        'movies').prefetch_related('actors').prefetch_related('directors').all()
    serializer_class = NewsSerializer
    pagination_class = NewsPagination

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.select_related('director').prefetch_related('actors').prefetch_related('category_set').all()
    serializer_class = MovieSerializer
    pagination_class = MoviePagination

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()


class DirctorViewSet(ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class SeasonViewSet(ModelViewSet):
    queryset = Series_season.objects.select_related('series').all()
    serializer_class = SeasonSerializer

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class EpisodeViewSet(ModelViewSet):
    queryset = Series_episode.objects.select_related('season').all()
    serializer_class = EpisodeSerializer

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.select_related('profile').select_related('movie').all()
    serializer_class = RatingSerializer
    permission_classes = [RatingPermission]

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()