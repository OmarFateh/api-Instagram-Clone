from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions

from item.models import Item
from explore.models import Hashtag
from item.serializers import ItemCreateSerializer, ItemListSerializer


class ExploreItemsAPIView(generics.ListAPIView):
    """
    Display all item of other users whose profiles are not privat, and not in user's following list.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ItemListSerializer
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}
        
    def get_queryset(self, *args, **kwargs):
        user = self.request.user.userprofile 
        # explore items
        return Item.objects.explore(user)   


class HashtagItemsAPIView(generics.ListAPIView):
    """
    Display all items that have a certain hashtag.
    """
    serializer_class = ItemListSerializer
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}
        
    def get_object(self, *args, **kwargs):
        # get hashtag slug from the requested url.
        hashtag_slug = self.kwargs.get("hashtag_slug", None)
        # get the hashtag object by slug.
        obj = get_object_or_404(Hashtag, slug=hashtag_slug)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self, *args, **kwargs):
        # hashtag items
        return Item.objects.filter(hashtags=self.get_object())    