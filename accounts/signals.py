from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from profiles.models import UserProfile


@receiver(post_save, sender=User)     # receiver(signal, **kwargs) # to register a signal
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create an empty profile once the user signed up.
    """
    if created:
        UserProfile.objects.create(user=instance)   