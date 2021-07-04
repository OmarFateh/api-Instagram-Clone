from rest_framework import serializers

from item.utils import datetime_to_string, rounded_timesince


class ItemLikesCommentsCountMixinSerializer(serializers.Serializer):
    """
    Item likes comments count mixin serializer.
    """
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class TimestampMixinSerializer(serializers.Serializer):
    """
    Timestamp mixin serializer.
    """
    updated_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()

    def get_updated_at(self, obj):
        return datetime_to_string(obj.updated_at)

    def get_created_at(self, obj):
        return datetime_to_string(obj.created_at)

    def get_timesince(self, obj):
        return f"{rounded_timesince(obj.created_at)} ago" 