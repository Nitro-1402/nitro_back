from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('comments', views.CommentViewSet, basename='comment')
router.register('likes', views.LikeCommentViewSet, basename='like')

urlpatterns = [
    path('',include(router.urls)),
]