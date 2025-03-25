from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('tasks', views.TaskViewSet, basename='tasks') # task-list, #task-detail
router.register('category', views.CategoryViewSet, basename='category')

# URLConf
urlpatterns = router.urls
