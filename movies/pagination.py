from rest_framework.pagination import PageNumberPagination

class CategoryPagination(PageNumberPagination):
    page_size = 4

class MoviePagination(PageNumberPagination):
    page_size = 20

class NewsPagination(PageNumberPagination):
    page_size = 8