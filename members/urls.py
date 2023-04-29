from django.urls import path, include
from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')
router.register('followers', views.FollowersListViewSet, basename='followers')
router.register('followings', views.FollowingsListViewSet, basename='followings')
router.register('follow', views.AddFollowViewSet, basename='follow')


urlpatterns = [
    path('',include(router.urls)),
    path('unfollow/', views.DeleteFollowViewSet.as_view(), name='unfollow'),
]