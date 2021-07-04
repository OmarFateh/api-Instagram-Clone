from django.dispatch import receiver
from django.db.models.signals import post_save

from notifications.models import Notification
from .models import FollowRequest


@receiver(post_save, sender=FollowRequest)     # receiver(signal, **kwargs) # to register a signal
def add_to_following(sender, instance, created, **kwargs):
    """
    Add profile to following and create follow notification once the friend request is accepted.
    Set notification to be inactive with declined as a status  once the friend request is declined.
    """
    sender_= instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.following.add(receiver_.user)
        # update notification to have accepted as a status and to be inactive.
        Notification.objects.filter(sender=sender_, receiver=receiver_, 
            status='sent', notification_type='follow_request').update(status='accepted', is_active=False)
        # create a follow type notification. 
        Notification.objects.create(sender=sender_, receiver=receiver_, notification_type='follow')        
    elif instance.status == 'declined':
        # update notification to have declined as a status and to be inactive.
        Notification.objects.filter(sender=sender_, receiver=receiver_, 
            status='sent', notification_type='follow_request').update(status='declined', is_active=False)