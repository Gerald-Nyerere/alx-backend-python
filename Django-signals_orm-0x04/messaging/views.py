from django.shortcuts import render, get_object_or_404
from .models import Message

# Create your views here.

def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    history = message.history.all()  
    return render(request, "messaging/message_detail.html", {"message": message,"history": history})
