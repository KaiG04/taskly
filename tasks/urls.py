from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('cards', views.TaskCardViewSet, basename='cards')
router.register('category', views.CategoryViewSet, basename='category')

# URLConf
urlpatterns = router.urls
