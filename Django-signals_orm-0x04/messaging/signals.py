from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
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


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    After a User is deleted, clean up related objects if not already cascaded.
    """
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(edited_by=instance).update(edited_by=None)

    print(f"🗑️ Cleaned up data for deleted user: {instance.username}")
