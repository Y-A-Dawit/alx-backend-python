from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log user out before deleting
    user.delete()    # Triggers post_delete signal
    return redirect('/')  # Redirect to home page after deletion

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_messages_with_replies(request):
    """
    Retrieve top-level messages (no parent) for the user
    and include replies in a threaded format.
    """
    # ✅ Use select_related + prefetch_related
    messages = Message.objects.filter(
        sender=request.user,
        parent_message__isnull=True
    ).select_related('sender', 'receiver')\
     .prefetch_related('replies')

    def recursive_replies(message):
        return [
            {
                "id": reply.id,
                "sender": reply.sender.username,
                "receiver": reply.receiver.username,
                "content": reply.content,
                "timestamp": reply.timestamp,
                "replies": recursive_replies(reply),
            }
            for reply in message.replies.all()
        ]

    # Build full tree for each top-level message
    data = []
    for msg in messages:
        data.append({
            "id": msg.id,
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
            "replies": recursive_replies(msg),
        })

    return Response(data)