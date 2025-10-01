from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
# Create your views here.

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