from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView,RetrieveAPIView
from .models import *
from .serializers import *


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = EditProfileSerializer

class FollowersListViewSet(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = FollowersSerializer


