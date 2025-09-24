from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view or modify that conversation or its messages.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        elif hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()
        return False
