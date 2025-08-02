from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # For demonstration of SerializerMethodField

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'role', 'full_name'
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
    participant_usernames = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )
    messages = MessageSerializer(many=True, read_only=True, source='message_set')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_usernames', 'messages', 'created_at']

    def validate(self, data):
        if 'participant_usernames' in data and len(data['participant_usernames']) < 2:
            raise serializers.ValidationError("At least two valid users are required.")
        return data
    
    def create(self, validated_data):
        usernames = validated_data.pop('participant_usernames')
        users = User.objects.filter(username__in=usernames)

        if users.count() < 2:
            raise serializers.ValidationError("At least two valid users are required.")
        
        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        return conversation
