from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')
router.register('followers', views.FollowersListViewSet, basename='followers')
router.register('followings', views.FollowingsListViewSet, basename='followings')
router.register('follow', views.AddFollowViewSet, basename='follow')
router.register('post', views.PostViewSet, basename='post')
router.register('subscribe', views.AddSubscriberViewSet, basename='subscribe')
router.register('subscribers', views.SubscribersViewSet, basename='subscribers')

urlpatterns = [
    path('',include(router.urls)),
    path('unfollow/', views.DeleteFollowView.as_view(), name='unfollow'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair_with_user'),
    path('unsubscribe/', views.DeleteSubscribeView.as_view(), name='unsubscribe')
]