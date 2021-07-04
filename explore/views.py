from django.shortcuts import get_object_or_404

from item.models import Item
from explore.models import Hashtag
from item.serializers import ItemCreateSerializer, ItemListSerializer

from rest_framework import generics


class ExploreItemsAPIView(generics.ListAPIView):
    """
    Display all item of other users whose profiles are not privat, and not in user's following list.
    """
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
        # get hashtag id from the requested url.
        hashtag_id = self.kwargs.get("hashtag_id", None)
        # get the hashtag object by id.
        obj = get_object_or_404(Hashtag, id=hashtag_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self, *args, **kwargs):
        # hashtag items
        return Item.objects.filter(hashtags=self.get_object())    