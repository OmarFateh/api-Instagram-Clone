from django.contrib.auth.models import User 

from profiles.models import UserProfile, FollowRequest
from accounts.serializers import UserSerializer
from .mixins import FollowCountMixinSerializer, IsFollowingMixinSerializer

from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer, FollowCountMixinSerializer, IsFollowingMixinSerializer):
    """
    A User profile serialzier.
    """
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    items_count = serializers.SerializerMethodField(read_only=True)
    followers_url = serializers.HyperlinkedIdentityField(view_name='profiles-api:followers', lookup_field='id')
    following_url = serializers.HyperlinkedIdentityField(view_name='profiles-api:following', lookup_field='id')

    class Meta:
        model  = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'photo', 'bio', 'following_count',
            'followers_count', 'items_count', 'is_following', 'followers_url', 'following_url', 'facebook',
            'twitter', 'website', 'private_account', 'updated_at', 'created_at'] 
        
    def validate_username(self, value):
        """
        Validate username.
        """
        username = value
        request = self.context['request']
        # check if the username has already been used.    
        user_username_qs = User.objects.filter(username__iexact=username).exclude(username=request.user)
        if user_username_qs.exists():
            raise serializers.ValidationError("This Username has already been used before!")
        return value

    def validate_email(self, value):
        """
        Validate email.
        """
        email = value
        request = self.context['request']
        # check if the email has already been used.    
        user_email_qs = User.objects.filter(email__iexact=email).exclude(email=request.user.email)
        if user_email_qs.exists():
            raise serializers.ValidationError("This Email has already been used before!")
        return value

    def update(self, instance, validated_data):
        request = self.context['request']
        # update user
        user = validated_data.get('user')
        instance.user.username = user.get('username')
        instance.user.first_name = user.get('first_name')
        instance.user.last_name = user.get('last_name')
        instance.user.email = user.get('email')
        instance.user.save()
        # update instance
        instance.photo = validated_data.get('photo', instance.photo)
        instance.bio = validated_data.get('bio')
        instance.facebook = validated_data.get('facebook')
        instance.twitter = validated_data.get('twitter')
        instance.website = validated_data.get('website')
        instance.private_account = validated_data.get('private_account')
        instance.save()
        return instance
  
    def get_items_count(self, obj):
        return obj.user.items.count()
    

class UserFollowersTagSerializer(serializers.ModelSerializer, IsFollowingMixinSerializer):
    """
    User followers tag list serializer.
    """
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    profile_url = serializers.HyperlinkedIdentityField(view_name='profiles-api:detail', lookup_field='id')

    class Meta:
        model  = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'photo', 'is_following', 'profile_url']


class UserFollowingSerializer(serializers.ModelSerializer):
    """
    User following list serialzier.
    """
    photo = serializers.SerializerMethodField(read_only=True)
    profile_url = serializers.HyperlinkedIdentityField(view_name='profiles-api:detail', lookup_field='id')
    
    class Meta:
        model  = User
        fields = ['id', 'username', 'first_name', 'last_name', 'photo', 'profile_url'] 

    def get_photo(self, obj):
        request = self.context["request"]
        try:
            return request.build_absolute_uri(obj.userprofile.photo.url)
        except:
            return request.build_absolute_uri(obj.photo.url)    


class UserFollowRequestSerializer(serializers.ModelSerializer):
    """
    User follow requests list serializer.
    """
    sender = UserFollowersTagSerializer()

    class Meta:
        model  = FollowRequest
        fields = ['id', 'sender']
