from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, MessageHistory

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = ['id', 'message', 'old_content', 'edited_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer()
    parent_message = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), allow_null=True, required=False)
    history = MessageHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'receiver',
            'content', 'timestamp', 'edited', 'edited_by',
            'parent_message', 'history'
        ]
