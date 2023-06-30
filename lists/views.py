from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.permissions import *
from rest_framework.decorators import action
from rest_framework import mixins
from .models import *
from .serializers import *
from .permissions import *
from members.models import Profile


class AddWatchedListViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = Watchedlist.objects.select_related('user_id').select_related('movie_id').all()
    serializer_class = AddWatchedListSerializer
    permission_classes = [AddToPermission]

    @action(detail=False, methods=['DELETE'], permission_classes=[DeletePermission])
    def delete(self, request):
        movie_id = request.GET.get('movie')
        profile_id = request.GET.get('profile')

        like = get_object_or_404(Watchedlist, movie=movie_id, profile=profile_id)
        like.delete()

        return Response({'message': 'watched movie deleted'}, status=status.HTTP_204_NO_CONTENT)

class RetrieveWatchedListViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('watched_list__movie').all()
    serializer_class = RetrieveWatchedListSerializer

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

class AddFavouritesViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = Favourites.objects.select_related('user_id').select_related('movie_id').all()
    serializer_class = AddFavouritesSerializer
    permission_classes = [AddToPermission]

    @action(detail=False, methods=['DELETE'], permission_classes=[DeletePermission])
    def delete(self, request):
        movie_id = request.GET.get('movie')
        profile_id = request.GET.get('profile')

        like = get_object_or_404(Favourites, movie=movie_id, profile=profile_id)
        like.delete()

        return Response({'message': 'favourite movie deleted'}, status=status.HTTP_204_NO_CONTENT)

class RetrieveFavouritesViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('favourites').all()
    serializer_class = RetrieveFavouritesSerializer

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

class AddBookmarksViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = Bookmarks.objects.select_related('user_id').select_related('movie_id').all()
    serializer_class = AddBookmarksSerializer
    permission_classes = [AddToPermission]

    @action(detail=False, methods=['DELETE'], permission_classes=[DeletePermission])
    def delete(self, request):
        movie_id = request.GET.get('movie')
        profile_id = request.GET.get('profile')

        like = get_object_or_404(Bookmarks, movie=movie_id, profile=profile_id)
        like.delete()

        return Response({'message': 'bookmarked movie deleted'}, status=status.HTTP_204_NO_CONTENT)

class RetrieveBookmarksViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('bookmarks').all()
    serializer_class = RetrieveBookmarksSerializer

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
        
class SuggestionsViewSet(mixins.ListModelMixin,GenericViewSet):
    queryset =Watchedlist.objects.annotate(count = Count('movie_id')).order_by('-count')[:5]
    serializer_class = SuggestionsSerializer