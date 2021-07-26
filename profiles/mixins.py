from rest_framework import serializers

from profiles.models import UserProfile


class UserInfoMixinSerializer(serializers.Serializer):
    """
    User info mixin serializer.
    """
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')


class ProfilePhotoMixinSerializer(serializers.Serializer):
    """
    Profile photo mixin serializer.
    """
    photo = serializers.SerializerMethodField(read_only=True)

    def get_photo(self, obj):
        request = self.context["request"]
        try:
            return request.build_absolute_uri(obj.userprofile.photo.url)
        except:
            return request.build_absolute_uri(obj.photo.url)


class FollowCountMixinSerializer(serializers.Serializer):
    """
    Follow count mixin serializer.
    """
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.get_followers.count()  


class IsFollowingMixinSerializer(serializers.Serializer):
    """
    Check if the current user is following a profile.
    """
    is_following = serializers.SerializerMethodField()

    def get_is_following(self, obj):
        request = self.context["request"]
        is_following = False
        if request.user.is_authenticated:
            is_following = request.user.userprofile in obj.user.followers.all()
        return is_following