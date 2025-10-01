from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message

# Create your views here.
@login_required
def send_message(request, receiver_id, parent_id=None):
    """
    Allows the logged-in user to send a message.
    Optionally links the message as a reply to another.
    """
    receiver = get_object_or_404(User, id=receiver_id)
    parent_message = None

    if parent_id:
        parent_message = get_object_or_404(Message, id=parent_id)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content, parent_message=parent_message)
            return redirect("inbox")  

    return render(request, "messaging/send_message.html", {"receiver": receiver, "parent_message": parent_message })

@login_required
def delete_user(request):
    """
    Allow a user to delete their own account.
    """
    if request.method == "POST":
        request.user.delete()
        return redirect("home")  
    return redirect("profile")  


def inbox(request):
    messages = (
        Message.objects.filter(parent_message__isnull=True)
        .select_related("sender", "receiver")
        .prefetch_related("replies__sender", "replies__receiver")
    )
    return render(request, "messaging/inbox.html", {"messages": messages})

@login_required
def unread_inbox(request):
    """
    Show unread messages for the logged-in user.
    """
    unread_messages = (
        Message.objects
        .filter(receiver=request.user, read=False)
        .select_related("sender")
        .only("id", "content", "created_at", "sender__username") 
    )

    return render(request, "messaging/unread_inbox.html", {"unread_messages": unread_messages})


@login_required
def read_message(request, message_id):
    """
    Mark a message as read when a receiver opens it.
    Use update_fields for an efficient update.
    """
    message = get_object_or_404(Message, id=message_id, receiver=request.user)
    if not message.read:
        message.read = True
        message.save(update_fields=["read"])
    return render(request, "messaging/read_message.html", {"message": message})










