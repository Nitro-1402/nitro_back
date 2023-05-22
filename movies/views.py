from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import *
from rest_framework.filters import SearchFilter , OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .pagination import *
from .permissions import *
from .filters import *

class NewsViewSet(ModelViewSet):
    queryset = News.objects.prefetch_related(
        'movies').prefetch_related('actors').prefetch_related('directors').all()
    serializer_class = NewsSerializer
    pagination_class = NewsPagination
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter , DjangoFilterBackend , OrderingFilter]
    ordering_fields = ['rating' , 'publish_date']
    search_fields = ['title' , 'director__name' , 'actors__name']   
    filterset_class = MovieFilter

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
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]

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