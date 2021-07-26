from rest_framework import permissions

from profiles.models import UserProfile
from item.models import Comment, Item


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = "You have to be the owner to apply action for this item."

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view it.
    Assumes the model instance has an `owner` attribute.
    """
    message = "You have to be the owner to view this item."

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsPrivateProfile(permissions.BasePermission):
    """
    Object-level permission to only allow followers to view account's data if private account.
    """
    message = "This account is private. Follow this account to view his photos."

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, UserProfile):
            is_private_account = obj.private_account
            user_followers = obj.get_followers
        elif isinstance(obj, Item):  
            is_private_account = obj.owner.userprofile.private_account
            user_followers = obj.owner.userprofile.get_followers
        elif isinstance(obj, Comment):
            is_private_account = obj.item.owner.userprofile.private_account
            user_followers = obj.item.owner.userprofile.get_followers        
        if is_private_account:
            return obj.owner == request.user or request.user in user_followers
        else:    
            return True