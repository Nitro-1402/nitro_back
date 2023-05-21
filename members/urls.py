from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('profiles', views.ProfileViewSet, basename='profiles')
router.register('followers', views.FollowersListViewSet, basename='followers')
router.register('followings', views.FollowingsListViewSet, basename='followings')
router.register('follow', views.AddFollowViewSet, basename='follow')
router.register('posts', views.PostViewSet, basename='post')
router.register('subscribe', views.AddSubscriberViewSet, basename='subscribe')
router.register('subscribers', views.SubscribersViewSet, basename='subscribers')

profiles_router = routers.NestedDefaultRouter(router, 'profiles', lookup='profile')
profiles_router.register('premiumPosts', views.PremiumPostViewSet, basename='profile-premiumPosts')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(profiles_router.urls)),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair_with_user'),
]