from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('addWatchedList', views.AddWatchedListViewSet, basename='addWatchedList')
router.register('watchedList', views.RetrieveWatchedListViewSet, basename='watchedList')
router.register('addFavourites', views.AddFavouritesViewSet, basename='addFavourites')
router.register('Favourites', views.RetrieveFavouritesViewSet, basename='favourites')
router.register('addBookmarks', views.AddBookmarksViewSet, basename='addBookmarks')
router.register('bookmarks', views.RetrieveBookmarksViewSet, basename='bookmarks')


urlpatterns = [
    path('',include(router.urls)),
]