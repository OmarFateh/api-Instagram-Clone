from django.shortcuts import get_object_or_404

from item.models import Item, Comment
from notifications.models import Notification
from accounts.serializers import UserSerializer
from profiles.permissions import IsOwnerOrReadOnly
from .serializers import (
        ItemCreateSerializer, 
        ItemDetailSerializer, 
        CommentDetailSerializer,
        CommentReplyDetailSerializer,
    )

from rest_framework import generics, mixins, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response


class ItemCreateAPIView(generics.CreateAPIView):
    """
    Item create API view.
    """
    queryset = Item.objects.all()
    serializer_class = ItemCreateSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ItemDetailUpdateDeleteAPIView(
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin, 
                generics.RetrieveAPIView
            ):
    """
    Item detail update delete API view. 
    Only the owner of the item can update or delete it, otherwise it will be displayed only.
    """
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer
    lookup_field = 'id'
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}
 
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)    


class LikeUnlikeItemAPIView(APIView):
    """
    Like and unlike item API view.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        # get item id from the requested url.
        item_id = self.kwargs.get("id", None)
        # get the item object by id
        obj = get_object_or_404(Item.objects.select_related('owner').prefetch_related('hashtags', 'tags', 'likes', 'favourites'), id=item_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        """
        Like or unlike item and send notification for the item's owner.
        """ 
        item = self.get_object()
        sender = request.user.userprofile
        receiver = item.owner.userprofile
        if item.likes.filter(id=request.user.id).exists():
            item.likes.remove(request.user)
            if sender != receiver:
                # set the item like notification to be inactive.
                Notification.objects.set_inactive(sender=sender, receiver=receiver, notification_type='like', item=item)
            return Response({'success':'you unliked this item successfully.'}, status=status.HTTP_200_OK)
        else:    
            item.likes.add(request.user)
            if sender != receiver:
                # create a like notification for this item with user as a sender, and profile as a receiver.  
                Notification.objects.create(sender=sender, receiver=receiver, item=item, notification_type='like')
            return Response({'success':'you liked this item successfully.'}, status=status.HTTP_200_OK)


class ItemLikesListAPIView(generics.ListAPIView):
    """
    Display a list of users who liked the item.
    """
    serializer_class = UserSerializer

    def get_object(self, *args, **kwargs):
        # get item id from the requested url.
        item_id = self.kwargs.get("id", None)
        # get the item object by id.
        obj = get_object_or_404(Item.objects.select_related('owner').prefetch_related('hashtags', 'tags', 'likes', 'favourites'), id=item_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get item likes queryset.
        return self.get_object().likes.all()


class AddDeleteItemFavouriteAPIView(APIView):
    """
    Add delete item favourite list API view.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        # get item id from the requested url.
        item_id = self.kwargs.get("id", None)
        # get the item object by id
        obj = get_object_or_404(Item.objects.select_related('owner').prefetch_related('hashtags', 'tags', 'likes', 'favourites'), id=item_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        """
        Add or delete item to or from the user's favourite list.
        """ 
        # add favourite to the item object by the user
        item = self.get_object()
        if item.favourites.filter(id=request.user.id).exists():
            item.favourites.remove(request.user)
            return Response({'success':'this item was deleted successfully from your favourite list.'}, status=status.HTTP_200_OK)
        else:    
            item.favourites.add(request.user)
            return Response({'success':'this item was added successfully to your favourite list.'}, status=status.HTTP_200_OK)


class ItemFavouritesListAPIView(generics.ListAPIView):
    """
    Display a list of users who added the item to favourite.
    """
    serializer_class = UserSerializer

    def get_object(self, *args, **kwargs):
        # get user id from the requested url.
        item_id = self.kwargs.get("id", None)
        # get the item object by id
        obj = get_object_or_404(Item.objects.select_related('owner').prefetch_related('hashtags', 'tags', 'likes', 'favourites'), id=item_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get item favourites queryset.
        return self.get_object().favourites.all()


class ItemCommentsListCreateAPIView(generics.ListCreateAPIView):
    """
    Display Item comments list, and create comment on the item.
    """
    serializer_class = CommentDetailSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def get_object(self, *args, **kwargs):
        # get item id from the requested url.
        item_id = self.kwargs.get("id", None)
        # get the item object by id.
        obj = get_object_or_404(Item.objects.select_related('owner').prefetch_related('hashtags', 'tags', 'likes', 'favourites'), id=item_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get item parent comments queryset.
        return self.get_object().parent_comments()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Override the perform create function and let the item owner be the requested user,
        and the item be the current item before saving. 
        """
        serializer.save(owner=self.request.user, item=self.get_object())    


class CommentRepliesListCreateAPIView(generics.ListCreateAPIView):
    """
    Display comment's replies list, and create reply for this comment.
    """
    serializer_class = CommentReplyDetailSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def get_object(self, *args, **kwargs):
        # get comment id from the requested url.
        comment_id = self.kwargs.get("id", None)
        # get the comment object by id.
        obj = get_object_or_404(Comment, id=comment_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self, *args, **kwargs):
        # get comment's replies queryset.
        comment = self.get_object()
        return Comment.objects.get_comment_replies(comment_id=comment.id, item_id=comment.item.id)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Override the perform create function and let the item owner be the requested user,
        the comment be the parent comment, and the item be the current item before saving. 
        """
        serializer.save(owner=self.request.user, reply=self.get_object(), item=self.get_object().item) 


class CommentDetailUpdateDeleteAPIView(
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin, 
                generics.RetrieveAPIView
            ):
    
    """
    Comment detail update delete API view.
    Only the owner of the comment can update or delete it, otherwise it will be displayed only.
    """
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    lookup_field = 'id'

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}
 
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
        
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)            


class LikeUnlikeCommentAPIView(APIView):
    """
    Like and unlike comment API view.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        # get comment id from the requested url.
        comment_id = self.kwargs.get("id", None)
        # get the comment object by id
        obj = get_object_or_404(Comment.objects.select_related('owner', 'item', 'reply').prefetch_related('likes'), id=comment_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        """
        Like or unlike comment and send notification for the comment's owner.
        """ 
        comment = self.get_object()
        sender = request.user.userprofile
        receiver = comment.owner.userprofile
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            if sender != receiver:
                # set the comment like notification to be inactive.
                Notification.objects.set_inactive(sender=sender, receiver=receiver, notification_type='comment_like', item=comment.item, comment=comment)
            return Response({'success':'you unliked this comment successfully.'}, status=status.HTTP_200_OK)
        else:    
            comment.likes.add(request.user)
            if sender != receiver:
                # create a like notification for this comment with user as a sender, and profile as a receiver.  
                Notification.objects.create(sender=sender, receiver=receiver, item=comment.item, comment=comment, notification_type='comment_like')
            return Response({'success':'you liked this comment successfully.'}, status=status.HTTP_200_OK)


class CommentLikesListAPIView(generics.ListAPIView):
    """
    Display a list of users who liked this comment.
    """
    serializer_class = UserSerializer

    def get_object(self, *args, **kwargs):
        # get comment id from the requested url.
        comment_id = self.kwargs.get("id", None)
        # get the item object by id.
        obj = get_object_or_404(Comment.objects.select_related('owner', 'item', 'reply').prefetch_related('likes'), id=comment_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get comment likes queryset.
        return self.get_object().likes.all()