from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import *


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.select_related('user').prefetch_related('Follows').all()
    serializer_class = EditProfileSerializer

# class FollowersListViewSet(ListAPIView):
#     queryset = 


