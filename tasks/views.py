from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Task, TaskBoard
from .permissions import TaskBoardAccess, IsTaskBoardOwner
from .serializers import TaskSerializer, TaskBoardSerializer

from .tasks import notify_user_invitation_to_task_board


# Create your views here.
class TaskBoardViewSet(ModelViewSet):
    serializer_class = TaskBoardSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskBoard.objects.filter(owner=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        # Django calls list method after getting the get request. Completes this and continues with original method.
        """
        Override the list method to ensure proper redirection if the request username doesn't match.
        """
        url_username = self.kwargs.get('username')

        # If the URL username doesn't match the logged-in user, redirect to their own boards
        if request.user.username != url_username:
            return redirect(f"/{request.user.username}/boards/")  # Redirect to correct user's boards

        # Call the original list method to return the task boards
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Override the retrieve method to ensure proper redirection if the request username doesn't match.
        """
        url_username = self.kwargs.get('username')
        slug = self.kwargs.get('slug')

        if request.user.username != url_username:
            return redirect(f"/{request.user.username}/boards/{slug}/")

        return super().retrieve(request, *args, **kwargs)



class TaskViewSet(ModelViewSet):
    #TODO Check TaskBoardVisibility Permission & Write Tests for it
    permission_classes = [TaskBoardAccess]
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

class InviteUserView(APIView):
    permission_classes = [IsAuthenticated, IsTaskBoardOwner]

    def post(self, request, *args, **kwargs):
        User = get_user_model()

        task_board = get_object_or_404(TaskBoard, slug=self.kwargs['board_slug'])
        username = request.data.get('username')
        action = request.data.get('action')

        if not action or action not in ['invite', 'remove']:
            return Response({'error': 'Invalid or missing action'}, status=status.HTTP_400_BAD_REQUEST)
        if not username:
            return Response({"Error: Username Required"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user != task_board.owner:
            return Response({"Error: Only the board owner can edit the guest list"}, status=status.HTTP_403_FORBIDDEN)

        action_user = get_object_or_404(User, username=username)

        if action == 'invite':
            if username == request.user.username:
                return Response({"Error: You cannot invite yourself!"}, status=status.HTTP_400_BAD_REQUEST)
            if task_board.guests.filter(
                    username=username).count():  # if username count > 1 (already in task board guests)
                return Response({"Error: User already invited!"}, status=status.HTTP_400_BAD_REQUEST)

            task_board.guests.add(action_user)
            notify_user_invitation_to_task_board(action_user, request.user, task_board)
            return Response({f"Message: {action_user.username} was successfully invited to '{task_board.title}'"},
                            status=status.HTTP_200_OK)

        if action == 'remove':
            if action_user.username == request.user.username:
                return Response({"Error: You cannot remove yourself!"}, status=status.HTTP_400_BAD_REQUEST)
            if action_user not in task_board.guests.all():
                return Response({"Error: User not a guest!"}, status=status.HTTP_400_BAD_REQUEST)
            task_board.guests.remove(action_user)
            return Response({f"Message: {action_user.username} was successfully removed from '{task_board.title}'"},)
        return Response({"Error: Invalid or missing action"}, status=status.HTTP_400_BAD_REQUEST)



