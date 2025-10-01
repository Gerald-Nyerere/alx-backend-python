from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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