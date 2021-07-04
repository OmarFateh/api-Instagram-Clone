from django.shortcuts import get_object_or_404

from rest_framework import generics

from item.models import Item, Comment
from profiles.models import UserProfile
from accounts.serializers import UserSerializer
from notifications.models import Notification
from .serializers import NotificationSerializer


class NotificationsListAPIView(generics.ListAPIView):
    """
    Display profile notifications.
    """
    serializer_class = NotificationSerializer

    def get_queryset(self, *args, **kwargs):
        # get profile of current user. 
        profile = get_object_or_404(UserProfile, user=self.request.user)    
        # get profile notifications.
        notifications_qs = Notification.objects.notifications_received(profile)
        # update profile notifications from not seen to seen. 
        Notification.objects.notifications_updated(profile)
        return notifications_qs

