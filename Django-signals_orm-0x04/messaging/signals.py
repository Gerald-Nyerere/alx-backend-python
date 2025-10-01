from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Signal to create a notification whenever a new Message is created.
    """
    if created:
        Notification.objects.create( user=instance.receiver, message=instance)
        print(f"🔔 Notification created for {instance.receiver.username} (Message from {instance.sender.username})")


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal that runs before a Message is updated.
    Saves old content to MessageHistory if the content is being changed.
    """
    if instance.pk: 
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                # Save old content to history
                MessageHistory.objects.create(message=instance, old_content=old_message.content)
                # Mark message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass