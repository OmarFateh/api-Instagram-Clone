from django.urls import path

from .views import ( 
        ItemCreateAPIView, 
        ItemDetailUpdateDeleteAPIView,
        LikeUnlikeItemAPIView,
        ItemLikesListAPIView,
        AddDeleteItemFavouriteAPIView,
        ItemFavouritesListAPIView,
        ItemCommentsListCreateAPIView,
        CommentDetailUpdateDeleteAPIView,
        CommentRepliesListCreateAPIView,
        LikeUnlikeCommentAPIView,
        CommentLikesListAPIView,
    )      

"""
CLIENT
BASE ENDPOINT /api/items/
"""

urlpatterns = [
 
    # item
    path('create/', ItemCreateAPIView.as_view(), name='create'),
    path('<int:id>/', ItemDetailUpdateDeleteAPIView.as_view(), name='detail'),
    
    # like 
    path('<int:id>/likes/add/', LikeUnlikeItemAPIView.as_view(), name='add-like'),
    path('<int:id>/likes/', ItemLikesListAPIView.as_view(), name='likes'),

    # favourite
    path('<int:id>/favourites/add/', AddDeleteItemFavouriteAPIView.as_view(), name='add-favourite'),
    path('<int:id>/favourites/', ItemFavouritesListAPIView.as_view(), name='favourites'),
    
    # comment
    path('<int:id>/comments/', ItemCommentsListCreateAPIView.as_view(), name='comments-list'),
    path('comments/<int:id>/', CommentDetailUpdateDeleteAPIView.as_view(), name='comments-detail'),
    path('comments/<int:id>/replies/', CommentRepliesListCreateAPIView.as_view(), name='replies-list'),

    # comment like
    path('comments/<int:id>/likes/add/', LikeUnlikeCommentAPIView.as_view(), name='add-comment-like'),
    path('comments/<int:id>/likes/', CommentLikesListAPIView.as_view(), name='comment-likes'),

]