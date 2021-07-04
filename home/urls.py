from django.urls import path

from .views import FeedItemsAPIView, TrendingItemsAPIView, ProfilesSuggestionsAPIView     

"""
CLIENT
BASE ENDPOINT /api/home/
"""

urlpatterns = [
    # feed items.
    path('', FeedItemsAPIView.as_view(), name='feed-items'),
    # trending items.
    path('trending/', TrendingItemsAPIView.as_view(), name='trending-items'),
    # suggested profiles
    path('suggestions/', ProfilesSuggestionsAPIView.as_view(), name='suggested-profiles'),
    
]