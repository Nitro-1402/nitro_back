from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework import mixins
from .models import *
from .serializers import *
from .permissions import *
from members.models import Profile

class AddWatchedListViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = Watchedlist.objects.select_related('user_id').select_related('movie_id').all()
    serializer_class = AddWatchedListSerializer
    permission_classes = [AddToPermission]

class RetrieveWatchedListViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('watched_list').all()
    serializer_class = RetrieveWatchedListSerializer

class AddFavouritesViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = Favourites.objects.select_related('user_id').select_related('movie_id').all()
    serializer_class = AddFavouritesSerializer
    permission_classes = [AddToPermission]


class RetrieveFavouritesViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('favourites').all()
    serializer_class = RetrieveFavouritesSerializer

class AddBookmarksViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = Bookmarks.objects.select_related('user_id').select_related('movie_id').all()
    serializer_class = AddBookmarksSerializer
    permission_classes = [AddToPermission]

class RetrieveBookmarksViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('bookmarks').all()
    serializer_class = RetrieveBookmarksSerializer