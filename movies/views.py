from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import *
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
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
                if self.request.user is not None:
                    return super().get_authenticators()
                else:
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
                if self.request.user is not None:
                    return super().get_authenticators()
                else:
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
                if self.request.user is not None:
                    return super().get_authenticators()
                else:
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

    def get_serializer_context(self):
        return {'request': self.request}

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                if self.request.user is not None:
                    return super().get_authenticators()
                else:
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
                if self.request.user is not None:
                    return super().get_authenticators()
                else:
                    return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()
        
class SeasonViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = SeasonSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Series_season.objects.filter(series_id=self.kwargs['movie_pk']).select_related('series').all()
    
    def get_serializer_context(self): 
        return {'movie_id': self.kwargs['movie_pk']}
    
    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class EpisodeViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Series_episode.objects.select_related('season').all()
    serializer_class = EpisodeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['season__season_number', 'season__series__title']
    permission_classes = [IsAdminOrReadOnly]

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                if self.request.user is not None:
                    return super().get_authenticators()
                else:
                    return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()

class RatingViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Rating.objects.select_related('profile').select_related('movie').all()
    serializer_class = RatingSerializer
    permission_classes = [RatingPermission]

    @action(detail=False, methods=['DELETE'])
    def delete(self, request):
        movie_id = request.data.get('movie')
        profile_id = request.data.get('profile')

        rating = get_object_or_404(Rating, movie=movie_id, profile=profile_id)
        rating.delete()

        return Response({'message': 'rating deleted'}, status=status.HTTP_204_NO_CONTENT)

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method in SAFE_METHODS:
                if self.request.user is not None:
                    return super().get_authenticators()
                else:
                    return []  
            else:
                return super().get_authenticators()
        else:
            return super().get_authenticators()