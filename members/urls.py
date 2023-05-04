from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')
router.register('followers', views.FollowersListViewSet, basename='followers')
router.register('followings', views.FollowingsListViewSet, basename='followings')
router.register('follow', views.AddFollowViewSet, basename='follow')


urlpatterns = [
    path('',include(router.urls)),
    path('unfollow/', views.DeleteFollowViewSet.as_view(), name='unfollow'),
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair_with_user_id')
]