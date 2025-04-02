from django.urls import path
from django.urls.conf import include

from .views import TaskCardViewSet, TaskViewSet

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views

router = DefaultRouter()
router.register(r'cards', TaskCardViewSet, basename='cards') #cards-list, cards-detail

cards_router = routers.NestedDefaultRouter(router, r'cards', lookup='card')
cards_router.register('tasks', TaskViewSet, basename='card-tasks')


# URLConf
urlpatterns = [
] + router.urls + cards_router.urls
