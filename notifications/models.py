from django.db import models
from django.urls import reverse

from item.models import BaseTimestamp


class NotificationManager(models.Manager):
    """
    Override the Notification manager.
    """
    def notifications_received(self, receiver):
        """
        Take a receiver, and return all his received notifications.
        """
        return Notification.objects.filter(receiver=receiver, is_active=True).exclude(sender=receiver)

    def notifications_count(self, receiver):
        """
        Take a receiver, and count his notifications.
        """
        return Notification.objects.filter(receiver=receiver, is_seen=False, is_active=True).exclude(sender=receiver).count()   

    def set_inactive(self, sender, receiver, notification_type, item=None, comment=None):
        """
        Take sender, receiver, notification_type, item, and comment.
        Set the notification to be inactive.
        """
        if item:
            return Notification.objects.filter(sender=sender, receiver=receiver, item=item,
                notification_type=notification_type, is_active=True).update(is_active=False)
        elif comment:
            return Notification.objects.filter(sender=sender, receiver=receiver, comment=comment,
                notification_type=notification_type, is_active=True).update(is_active=False)        
        else:
            return Notification.objects.filter(sender=sender, receiver=receiver, 
                notification_type=notification_type, is_active=True).update(is_active=False)

    def notifications_updated(self, receiver):
        """
        Take a receiver, and update his notifications after seeing them.
        """
        return Notification.objects.filter(receiver=receiver, is_seen=False).update(is_seen=True)

    def get_or_create_notification(self, sender, receiver, item, notification_type):
        """
        Take sender, receiver, item, and notification_type.
        Get the notification if it already exists, and if not, create a new notification.
        """
        # check and return the notification if already exists or not. 
        qs_get = self.get_queryset().filter(sender=sender, receiver=receiver, item=item, notification_type=notification_type)
        if qs_get.exists():
            # activate all notification that already exists
            qs_get.update(is_active=True)
            return qs_get.first(), False
        # create a new one.     
        return Notification.objects.create(sender=sender, receiver=receiver, item=item, notification_type=notification_type), True  
    
    def inactive_tag_notification(self, sender, item, notification_type):
        """
        Take sender, item, and notification_type.
        Inactive tag notification which is longer exists in the item's tags.
        """
        item_tags = item.tags.all()
        # get a queryset of tag notifications excluding the ones of the item and set them to be inactive.
        return self.get_queryset().filter(sender=sender, item=item, notification_type=notification_type, 
                    is_active=True).exclude(receiver__in=item_tags).update(is_active=False)   


class Notification(BaseTimestamp):
    """
    Notification model.
    """
    STATUS_CHOICES = (
        ('sent', 'sent'),
        ('accepted', 'accepted'),
        ('declined', 'declined'),
    )

    NOTIFICATION_TYPE = (
        ('like', 'like'),
        ('comment', 'comment'),
        ('follow', 'follow'),
        ('tag', 'tag'),
        ('follow_request', 'follow request'),
        ('comment_like', 'comment like'),
    )

    sender = models.ForeignKey("profiles.UserProfile", on_delete=models.CASCADE, related_name='noti_from_user')
    receiver = models.ForeignKey("profiles.UserProfile", on_delete=models.CASCADE, related_name='noti_to_user')
    item = models.ForeignKey("item.Item", on_delete=models.CASCADE, related_name='noti_item', blank=True, null=True)
    comment = models.ForeignKey("item.Comment", on_delete=models.CASCADE, related_name='noti_comment', blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, blank=True, null=True)
    notification_type = models.CharField(max_length=14, choices=NOTIFICATION_TYPE)
    comment_snippt = models.CharField(max_length=90, blank=True, null=True)
    is_seen = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
   
    objects = NotificationManager()
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # Return sender's username, receiver's username, and the notification type.
        return f'{self.sender}-{self.receiver}-{self.notification_type}'

    def get_invitation_accept_absolute_url(self):
        # Return absolute url of follow request acceptance.
        return reverse('notifications:invitation-accept')

    def get_invitation_delete_absolute_url(self):
        # Return absolute url of follow request deletion.
        return reverse('notifications:invitation-delete')     

    