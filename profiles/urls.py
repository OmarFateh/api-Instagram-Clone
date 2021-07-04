from django.urls import path

from .views import (
        UserProfileDetailUpdateAPIView,
        FollowUserAPIView,
        FollowRequestsListAPIView,
        AcceptFollowRequestAPIView,
        DeclineFollowRequestAPIView, 
        UserFollowersListAPIView,
        UserFollowingListAPIView,
        UserItemsListAPIView,
        UserItemsFavouritesListAPIView,
        UserItemsTaggedListAPIView,
    ) 

"""
CLIENT
BASE ENDPOINT /api/profiles/
"""

urlpatterns = [

    # profile detail
    path('<int:id>/', UserProfileDetailUpdateAPIView.as_view(), name='detail'),
    
    # follow
    path('<int:id>/follow/', FollowUserAPIView.as_view(), name='follow'),
    path('follow/requests/', FollowRequestsListAPIView.as_view(), name='follow-requests'),
    path('follow/requests/<int:id>/accept/', AcceptFollowRequestAPIView.as_view(), name='accept-request'),
    path('follow/requests/<int:id>/decline/', DeclineFollowRequestAPIView.as_view(), name='decline-request'),
    path('<int:id>/followers/', UserFollowersListAPIView.as_view(), name='followers'),
    path('<int:id>/following/', UserFollowingListAPIView.as_view(), name='following'),
    
    # items
    path('<int:id>/items/', UserItemsListAPIView.as_view(), name='items'),
    path('<int:id>/items/favourites/', UserItemsFavouritesListAPIView.as_view(), name='favourites'),
    path('<int:id>/items/tagged/', UserItemsTaggedListAPIView.as_view(), name='tagged')
]