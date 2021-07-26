from django.urls import path

from .views import ExploreItemsAPIView, HashtagItemsAPIView
         

"""
CLIENT
BASE ENDPOINT /api/explore/
"""

urlpatterns = [
    # explore items.
    path('', ExploreItemsAPIView.as_view(), name='explore-items'),
    # hashtags items.
    path('tags/<str:hashtag_slug>/', HashtagItemsAPIView.as_view(), name='hashtags-items'),
    
]