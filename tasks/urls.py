from django.urls import path
from django.urls.conf import include

from .views import TaskBoardViewSet, TaskViewSet

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('boards', TaskBoardViewSet, basename='taskboards')

tasks_router = routers.NestedSimpleRouter(router, r'boards', lookup='board')
tasks_router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('<str:username>/', include(router.urls)),
] + tasks_router.urls

