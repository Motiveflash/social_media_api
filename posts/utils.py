from .models import Notification

def create_notification(user, sender, post, notification_type, message):
    Notification.objects.create(
        user=user,
        sender=sender,
        post=post,
        notification_type=notification_type,
        message=message
    )
