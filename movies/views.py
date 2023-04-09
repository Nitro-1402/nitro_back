from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

class NewsViewSet(ModelViewSet):
    queryset = News.objects.prefetch_related(
        'movies').prefetch_related('actors').prefetch_related('directors').all()
    serializer_class = NewsSerializer
