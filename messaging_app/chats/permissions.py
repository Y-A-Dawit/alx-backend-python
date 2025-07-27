# messaging_app/chats/permissions.py

from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow users to access only their own messages/conversations.
    """

    def has_object_permission(self, request, view, obj):
        # Assumes 'owner' field on the object points to request.user
        return obj.owner == request.user
