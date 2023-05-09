from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('addWatchedList', views.AddWatchedListViewSet, basename='addWatchedList')
router.register('watchedList', views.RetrieveWatchedListViewSet, basename='watchedList')


urlpatterns = [
    path('',include(router.urls)),
]