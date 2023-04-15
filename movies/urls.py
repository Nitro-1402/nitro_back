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
router.register('seasons' , views.SeasonViewSet , basename='seasons')
router.register('episodes' , views.EpisodeViewSet , basename='episodes')


urlpatterns = router.urls