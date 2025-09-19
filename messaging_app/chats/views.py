from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import Conversation, Message
from .serializers import Conversationserializers, MessageSerializer

User = settings.AUTH_USER_MODEL


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = Conversationserializers
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at'] 

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def retrieve(self, request, pk=None):
        conversation = get_object_or_404(self.get_queryset(), conversation_id=pk)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages for a given conversation.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender_id__email']
    ordering_fields = ['sent_at']
    ordering = ['sent_at'] 

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_pk")
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        return conversation.messages.select_related("sender_id")

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_pk")
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        serializer.save(sender_id=self.request.user, conversation=conversation)
