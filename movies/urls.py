from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('news', views.NewsViewSet, basename='news')

urlpatterns = router.urls