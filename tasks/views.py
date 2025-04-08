from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet



from .models import Task, TaskBoard
from .permissions import IsOwnerOrReadOnly
from .serializers import TaskSerializer, TaskBoardSerializer


# Create your views here.
class TaskBoardViewSet(ModelViewSet):
    serializer_class = TaskBoardSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return TaskBoard.objects.filter(owner=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        # Django calls list method after getting the get request. Completes this and continues with original method.
        """
        Override the list method to ensure proper redirection if the username doesn't match.
        """
        url_username = self.kwargs.get('username')

        # If the URL username doesn't match the logged-in user, redirect to their own boards
        if request.user.username != url_username:
            return redirect(f"/{request.user.username}/boards")  # Redirect to correct user's boards

        # Call the original list method to return the task boards
        return super().list(request, *args, **kwargs)


class TaskViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    lookup_field = 'slug'
    search_fields = ['title']
    ordering_fields = ['created_at']
    serializer_class = TaskSerializer

    def get_queryset(self):
        board_slug = self.kwargs.get('board_slug')
        board = get_object_or_404(TaskBoard, slug=board_slug)
        return Task.objects.filter(task_board=board)


    def perform_create(self, serializer):
        task_board = TaskBoard.objects.get(slug=self.kwargs['board_slug'])
        task = serializer.save(created_by=self.request.user, task_board=task_board)
        task.save()
