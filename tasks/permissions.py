from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import TaskBoard

class TaskBoardAccess(BasePermission):
    def has_permission(self, request, view):
        board_id = view.kwargs.get('board_slug')
        if not board_id: # Find out a board exists
            return False

        board = get_object_or_404(TaskBoard, slug=board_id)

        if request.user == board.owner: return True
        if request.user in board.guests.all(): return True
        if request.method in SAFE_METHODS and request.user.is_authenticated and board.visibility == 'PUB': return True
        return False


    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and request.user.is_authenticated: return True
        if request.method in [*SAFE_METHODS, 'POST', 'PUT', 'PATCH', 'DELETE']:
            if request.user == obj.task_board.owner: return True
            if request.user in obj.task_board.guests.all(): return True
        return False

class IsTaskBoardOwner(BasePermission):
    def has_permission(self, request, view):
        board_slug = view.kwargs.get('board_slug')
        board = get_object_or_404(TaskBoard, slug=board_slug)

        if board.owner == request.user:
            return True
        return False






