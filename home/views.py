from rest_framework import generics

from item.models import Item
from profiles.models import UserProfile
from accounts.serializers import UserSerializer
from item.serializers import ItemListSerializer, ItemFeedListSerializer


class FeedItemsAPIView(generics.ListAPIView):
    """
    Display the items of the requested user and their followings, ordered by the latest created ones.
    """
    serializer_class = ItemFeedListSerializer
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}
        
    def get_queryset(self, *args, **kwargs):
        user = self.request.user.userprofile 
        # get items of the requested user and their followings.
        return Item.objects.feed(user)   


class TrendingItemsAPIView(generics.ListAPIView):
    """
    Display trending items, items with most likes in descending order.
    """
    serializer_class = ItemListSerializer
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}
        
    def get_queryset(self, *args, **kwargs):
        user = self.request.user.userprofile 
        # trending items. 
        return Item.objects.trending(user)[:6]    


class ProfilesSuggestionsAPIView(generics.ListAPIView):
    """
    Display the mutual profiles between the user and his following,
    and the profiles that are in user's followers but not in his following,
    orderd by the latest created ones.
    """
    serializer_class = UserSerializer
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}
        
    def get_queryset(self, *args, **kwargs):
        user = self.request.user.userprofile 
        # suggested profiles
        return UserProfile.objects.suggested_profiles(user)[:6]    