from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password_hash', 'phone_number', 'role']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(source="sender_id", read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "sender", "message_body", "sent_at"]


class Conversationserializers(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "created_at", "messages"]
