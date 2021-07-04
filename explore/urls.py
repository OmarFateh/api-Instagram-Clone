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
    path('tags/<int:hashtag_id>/', HashtagItemsAPIView.as_view(), name='hashtags-items'),
    
]