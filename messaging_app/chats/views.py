# chats/views.py

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwner, IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


#  Conversation ViewSet
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username', 'participants__email']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  #Task 1

    def get_queryset(self):
        #  Return conversations where user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)   # Create serializer with request data
        serializer.is_valid(raise_exception=True)             # Validate the data (raises 400 if invalid)
        self.perform_create(serializer)                       # Calls serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return created object


#  Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    search_fields = ['conversation__conversation_id', 'sender__id']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  #updated here

    def get_queryset(self):
        # Return only messages sent by the user
        return Message.objects.filter(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get('conversation_pk')
        sender_id = request.data.get('sender')
        message_body = request.data.get('message_body')

        if not all([conversation_id, sender_id, message_body]):
            return Response(
            {"error": "conversation, sender, and message_body are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            sender = User.objects.get(id=sender_id)
        except (Conversation.DoesNotExist, User.DoesNotExist):
            return Response(
            {"error": "Conversation or sender not found."},
            status=status.HTTP_404_NOT_FOUND
        )

        if request.user not in conversation.participants.all():
            return Response(
            {"error": "You are not a participant of this conversation."},
            status=status.HTTP_403_FORBIDDEN
        )

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
    )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
