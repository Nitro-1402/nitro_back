from django.urls import path, include
from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')
router.register('follow', views.AddFollowViewSet, basename='addfollow')
router.register('followers', views.FollowersListViewSet, basename='followers')

urlpatterns = router.urls