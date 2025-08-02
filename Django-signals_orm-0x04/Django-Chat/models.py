from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_received')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    
    # ✅ New field for threading
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"

    def get_all_replies(self):
        """
        Recursively fetch all replies in threaded format
        """
        def recursive_replies(message):
            result = []
            for reply in message.replies.all():
                result.append({
                    'id': reply.id,
                    'content': reply.content,
                    'sender': reply.sender.username,
                    'timestamp': reply.timestamp,
                    'replies': recursive_replies(reply)
                })
            return result

        return recursive_replies(self)
