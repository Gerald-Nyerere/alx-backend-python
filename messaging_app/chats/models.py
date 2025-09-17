import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'guest'),
        ('host', 'host'),
        ('admin', 'admin'),
    ]

    user_id = models.UUIDField(primary_key= True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    password_hash = models.CharField(max_length=255, null=False)
    phone_number = models.IntegerField(null=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name}"

class Message(models.Model):
    message_id = models.UUIDField(primary_key= True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    sender_id = models.ForeignKey(User, to_field='user_id', on_delete=models.CASCADE, related_name="sent_messages")
    message_body = models.CharField(max_length=255, null=False)
    sent_at  = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key= True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    sender_id = models.ForeignKey(User, to_field='user_id', on_delete=models.CASCADE, related_name="conversation_messages")
    created_at  = models.DateTimeField(auto_now_add=True)
