from profiles.models import UserProfile

from rest_framework import serializers


class FollowCountMixinSerializer(serializers.Serializer):
    """
    """
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.get_followers.count()  


class IsFollowingMixinSerializer(serializers.Serializer):
    """
    """
    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        request = self.context["request"]
        is_following = False
        if request.user.is_authenticated:
            is_following = request.user.userprofile in obj.user.followers.all()
        return is_following     