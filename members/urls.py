from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')
router.register('followers', views.FollowersListViewSet, basename='followers')
router.register('followings', views.FollowingsListViewSet, basename='followings')
router.register('follow', views.AddFollowViewSet, basename='follow')

profile_router = routers.NestedDefaultRouter(router, 'profile', lookup='profile')
profile_router.register('items', views.WatchedListViewSet, basename='profile-watched')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(profile_router.urls)),
    path('unfollow/', views.DeleteFollowViewSet.as_view(), name='unfollow'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair_with_user')
]