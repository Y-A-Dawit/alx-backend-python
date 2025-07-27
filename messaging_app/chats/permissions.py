# messaging_app/chats/permissions.py

from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow users to access only their own messages/conversations.
    """

    def has_object_permission(self, request, view, obj):
        # Assumes 'owner' field on the object points to request.user
        return obj.owner == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Allow only authenticated users
    - Allow only participants of a conversation to access it
    - For message updates/deletes, ensure user is the sender
    """

    def has_permission(self, request, view):
        # Must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Assumes the `Conversation` model has a ManyToMany field like:
        participants = models.ManyToManyField(User)
        """

        user = request.user
        
         # If the object is a Conversation
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        # If the object is a Message
        if hasattr(obj, 'conversation') and hasattr(obj, 'sender'):
            is_participant = user in obj.conversation.participants.all()
            if request.method in ["PUT", "PATCH", "DELETE"]:
                return is_participant and obj.sender == user
            return is_participant

        return False