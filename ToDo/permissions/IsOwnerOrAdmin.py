from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners and admins to view and edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff
