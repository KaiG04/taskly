from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import TaskBoard

class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_authenticated: # Checks for safe method and auth user
            return True

        board_id = view.kwargs.get('board_slug')
        if not board_id: # Find out a board exists
            return False

        try:
            board = TaskBoard.objects.get(slug=view.kwargs.get('board_slug'))
            return board.owner == request.user # Checks if board owner is request user bool return
        except TaskBoard.DoesNotExist:
            return False # Handles DNE error is TaskBoard does not exist returns 404 based on view.

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and request.user.is_authenticated: return True
        return bool(obj.task_board.owner == request.user)

class TaskBoardVisibility(BasePermission):
    def has_permission(self, request, view):
        board_slug = view.kwargs.get('board_slug')
        board = TaskBoard.objects.get(slug=board_slug)
        if board.visibility == "PRI":
            if request.user == board.owner:
                return True
            return False
        if board.visibility == "PUB":
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and request.user.is_authenticated: return True
        return bool(obj.task_board.owner == request.user)







