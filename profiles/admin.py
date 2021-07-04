from django.contrib import admin

from .models import UserProfile, UserFollow, FollowRequest


class UserFollowAdmin(admin.TabularInline):
    """
    Display the user follow model as a tabular inline. 
    """
    model = UserFollow


class UserProfileAdmin(admin.ModelAdmin):
    """
    Override the user profile admin and customize the user profiles display.
    """
    inlines = [UserFollowAdmin]
    # list_display  = []
    # search_fields = []

    class Meta:
        model = UserProfile


# models admin site registeration 
admin.site.register(UserProfile, UserProfileAdmin) 
admin.site.register(FollowRequest)      