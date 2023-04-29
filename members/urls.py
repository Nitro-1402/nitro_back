from django.urls import path, include
from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')

# urlpatterns_schema = [
#     path('schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
# ]
urlpatterns = [
    path('', include(router.urls)),
    path('followers', views.FollowersListViewSet.as_view(), name='followers')
]