from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework import mixins
from .models import *
from .serializers import *


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = EditProfileSerializer

class FollowersListViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('followers').all()
    serializer_class = FollowersSerializer

class FollowingsListViewSet(mixins.RetrieveModelMixin,GenericViewSet):
    queryset = Profile.objects.prefetch_related('followings').all()
    serializer_class = FollowingsSerializer

class AddFollowViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = UserFollow.objects.select_related('follower_id').select_related('following_id').all()
    serializer_class = AddFollowSerializer


