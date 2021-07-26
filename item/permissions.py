from rest_framework import permissions

from item.models import Comment, Item


class IsRestrictedComments(permissions.BasePermission):
    """
    Object-level permission to only allow comments to be added if the the item has no restrict comment option.
    """
    message = "Comments are restricted for this Item."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Item):
            return not obj.restrict_comment
        elif isinstance(obj, Comment):
            return not obj.item.restrict_comment