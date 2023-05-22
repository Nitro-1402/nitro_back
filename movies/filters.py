from django_filters.rest_framework import FilterSet
from .models import Movie

class MovieFilter(FilterSet):
    class Meta:
        model = Movie
        fields = {
            'movie_type' : ['exact'] ,
            'category_set': ['exact'] , 
            'rating' : ['gt' , 'lt'] , 
            'publish_date' : ['gt' , 'lt'] , 
            'country' : ['exact']
        }