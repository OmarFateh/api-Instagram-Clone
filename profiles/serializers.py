from django.contrib.auth.models import User 

from rest_framework import serializers

from profiles.models import UserProfile, FollowRequest
from .mixins import (UserInfoMixinSerializer, ProfilePhotoMixinSerializer, FollowCountMixinSerializer, 
                        IsFollowingMixinSerializer)


class UserProfileSerializer(serializers.ModelSerializer, UserInfoMixinSerializer, FollowCountMixinSerializer, 
                                IsFollowingMixinSerializer):
    """
    A User profile serialzier.
    """
    items_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model  = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'photo', 'bio', 'following_count',
            'followers_count', 'items_count', 'is_following', 'facebook', 'twitter', 'website', 
            'private_account', 'updated_at', 'created_at'] 
        
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
        instance.user.username = validated_data.get('username', instance.user.username)
        instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
        instance.user.last_name = validated_data.get('last_name', instance.user.last_name)
        instance.user.email = validated_data.get('email', instance.user.email)
        instance.user.save()
        return super().update(instance, validated_data)  
  
    def get_items_count(self, obj):
        return obj.user.items.count()
    

class UserFollowersTagSerializer(serializers.ModelSerializer, UserInfoMixinSerializer, IsFollowingMixinSerializer):
    """
    User followers tag list serializer.
    """
    class Meta:
        model  = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'photo', 'is_following']


class UserFollowingSerializer(serializers.ModelSerializer, ProfilePhotoMixinSerializer):
    """
    User following list serialzier.
    """    
    class Meta:
        model  = User
        fields = ['id', 'username', 'first_name', 'last_name', 'photo'] 


class UserFollowRequestSerializer(serializers.ModelSerializer):
    """
    User follow requests list serializer.
    """
    sender = UserFollowersTagSerializer()

    class Meta:
        model  = FollowRequest
        fields = ['id', 'sender']
