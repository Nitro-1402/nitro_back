from django.urls import path
from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

router = routers.DefaultRouter()
router.register('news', views.NewsViewSet, basename='news')
router.register('actors', views.ActorViewSet, basename='actors')
router.register('categories' , views.CategoryViewSet , basename='categories')
router.register('movies' , views.MovieViewSet ,basename='movies')
router.register('directors' , views.DirctorViewSet , basename='directors')

urlpatterns_schema = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
urlpatterns = router.urls + urlpatterns_schema