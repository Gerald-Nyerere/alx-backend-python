from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password_hash', 'phone_number', 'role']

        def get_full_name(self, obj):
            return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(source="sender_id", read_only=True)
    message_body = serializers.CharField(max_length=2000)

    class Meta:
        model = Message
        fields = ["message_id", "sender", "message_body", "sent_at"]

        def validate_message_body(self, value):
            if not value.strip():
                raise serializers.ValidationError("Message body cannot be empty.")
            if len(value) < 2:
                raise serializers.ValidationError("Message is too short.")
            return value


class ConversationSerializers(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "created_at", "messages"]

        def get_participant_count(self, obj):
            return obj.participants.count()
