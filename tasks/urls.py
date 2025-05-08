from django.urls import path
from django.urls.conf import include

from .views import TaskBoardViewSet, TaskViewSet, InviteUserView

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('boards', TaskBoardViewSet, basename='taskboards')

#/{username}/boards - board-list
#/{username}/boards/{board_id} board-detail
tasks_router = routers.NestedSimpleRouter(router, r'boards', lookup='board')

# /boards/{board_slug}/tasks
tasks_router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('<str:username>/', include(router.urls)),
    path('boards/<str:board_slug>/invite/', InviteUserView.as_view()),
] + tasks_router.urls

