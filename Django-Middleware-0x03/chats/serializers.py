from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # For demonstration of SerializerMethodField

    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name',
            'email', 'phone_number', 'role', 'created_at', 'full_name'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField()  # Explicit use
    sender_email = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_email', 'message_body', 'sent_at']

    def get_sender_email(self, obj):
        return obj.sender.email


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='message_set')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def validate(self, data):
        if 'participants' in data and len(data['participants']) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return data
