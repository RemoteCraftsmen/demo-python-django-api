"""
Permission to only allow owners of an object to view and edit it.
"""
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Allow access for edit and view only for owner
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
