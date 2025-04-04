from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow only task owners to edit, while allowing read access to everyone.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions (GET, HEAD, OPTIONS) are allowed for everyone
        if request.method in SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the task
        return obj.created_by == request.user



