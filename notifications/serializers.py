from notifications.models import Notification
from accounts.serializers import UserSerializer
from item.serializers import ItemListSerializer
from item.mixins import TimestampMixinSerializer

from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer, TimestampMixinSerializer):
    """
    Notification serializer.
    """
    sender = UserSerializer(read_only=True)
    item = ItemListSerializer(read_only=True)
    
    class Meta:
        model  = Notification
        fields = ['sender', 'item', 'comment', 'status', 'notification_type', 'comment_snippt', 'is_seen',
            'updated_at', 'created_at', 'timesince']
        read_only_fields = ['image']