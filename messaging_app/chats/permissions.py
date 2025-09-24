from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """
    Allows access only to participants of a conversation or messages within it.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()
        elif hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()
        return False
