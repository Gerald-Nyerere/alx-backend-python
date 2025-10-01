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