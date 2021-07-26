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
    path('<str:username>/', UserProfileDetailUpdateAPIView.as_view(), name='detail'),
    
    # follow
    path('<str:username>/follow/', FollowUserAPIView.as_view(), name='follow'),
    path('follow/requests/', FollowRequestsListAPIView.as_view(), name='follow-requests'),
    path('follow/requests/<int:id>/accept/', AcceptFollowRequestAPIView.as_view(), name='accept-request'),
    path('follow/requests/<int:id>/decline/', DeclineFollowRequestAPIView.as_view(), name='decline-request'),
    path('<str:username>/followers/', UserFollowersListAPIView.as_view(), name='followers'),
    path('<str:username>/following/', UserFollowingListAPIView.as_view(), name='following'),
    
    # items
    path('<str:username>/items/', UserItemsListAPIView.as_view(), name='items'),
    path('<str:username>/items/favourites/', UserItemsFavouritesListAPIView.as_view(), name='favourites'),
    path('<str:username>/items/tagged/', UserItemsTaggedListAPIView.as_view(), name='tagged')
]