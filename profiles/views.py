from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User 

from profiles.models import UserProfile, FollowRequest
from item.serializers import ItemListSerializer
from notifications.models import Notification
from .permissions import IsOwnerOrReadOnly
from .serializers import UserProfileSerializer, UserFollowingSerializer, UserFollowersTagSerializer, UserFollowRequestSerializer

from rest_framework import generics, permissions, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response


class UserProfileDetailUpdateAPIView(mixins.UpdateModelMixin, generics.RetrieveAPIView):
    """
    User profile detail update API view.
    Only the owner of the profile can update it, otherwise it will be displayed only.
    """
    permission_classes = [IsOwnerOrReadOnly]

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'
    
    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class FollowUserAPIView(APIView):
    """
    Follow and unfollow user API view.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, *args, **kwargs):
        # get user id from the requested url.
        user_id = self.kwargs.get("id", None)
        # get the user object by id
        obj = get_object_or_404(UserProfile, id=user_id)
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        """
        Follow or unfollow and send notification for the followed user.
        """ 
        profile_obj = self.get_object()
        user = request.user.userprofile
        # check if the profile is private or not.
        private_account = False
        if profile_obj.private_account and request.user.userprofile not in profile_obj.user.followers.all() and request.user != profile_obj.user:
            private_account = True
        # if the user is in profile's followers.
        if user in profile_obj.user.followers.all():
            if user != profile_obj: 
                # remove user from profile's followers.
                profile_obj.user.followers.remove(user)
                # set the follow notification to be inactive.
                Notification.objects.set_inactive(sender=user, receiver=profile_obj, notification_type='follow')
                return Response({'success':'you have unfollowed this account successfully.'}, status=status.HTTP_200_OK)    
        # if profile is private account    
        elif private_account:
            if user != profile_obj:
                # check if the user has already sent a follow request to this profile or not. 
                is_noti_exists = UserProfile.objects.is_request_sent(user, profile_obj)
                is_requested = FollowRequest.objects.filter(sender=user, receiver=profile_obj, status='sent').exists()
                if not is_requested and not is_noti_exists:
                    # create a follow request
                    FollowRequest.objects.create(sender=user, receiver=profile_obj, status='sent')
                    # create a follow request notification of sent as a status type with user as a sender, and profile as a receiver.  
                    Notification.objects.create(sender=user, receiver=profile_obj, status='sent', notification_type='follow_request')
                    return Response({'success':'you have sent a follow request to this account successfully.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'success':'you have already sent a follow request before to this account.'}, status=status.HTTP_200_OK)
        # if the user is not in profile's followers and profile is not private account.
        else:
            if user != profile_obj: 
                # add user to profile's followers.
                profile_obj.user.followers.add(user)
                # create a follow notification with user as a sender, and profile as a receiver. 
                Notification.objects.create(sender=user, receiver=profile_obj, notification_type='follow')      
                return Response({'success':'you have followed this account successfully.'}, status=status.HTTP_200_OK)
        return Response({'success':"you can't follow yourself."}, status=status.HTTP_200_OK)


class FollowRequestsListAPIView(generics.ListAPIView):
    """
    Display a list of follow requests.
    """
    serializer_class = UserFollowRequestSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def get_object(self, *args, **kwargs):
        # get the user profile object by id
        obj = get_object_or_404(UserProfile, id=self.request.user.userprofile.id)
        # check object permissions
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get user follow requests receieved queryset 
        return self.get_object().request_to_user.filter(status='sent')


class AcceptFollowRequestAPIView(APIView):
    """
    Accept follow rquests API view.
    Only the receiver of the request can accept it.
    """
    def get_object(self, *args, **kwargs):
        # get follow request id from the requested url.
        follow_id = self.kwargs.get("id", None)
        # get the follow request object by id.
        obj = get_object_or_404(FollowRequest, id=follow_id, receiver=self.request.user.userprofile, status='sent')
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        """
        Accept follow request.
        """  
        follow_request = self.get_object()   
        follow_request.status = 'accepted'
        follow_request.save() 
        return Response({'success':"you have accepted this follow request successfully."}, status=status.HTTP_200_OK)


class DeclineFollowRequestAPIView(APIView):
    """
    Decline follow rquests API view.
    Only the receiver of the request can decline it.
    """
    def get_object(self, *args, **kwargs):
        # get follow request id from the requested url.
        follow_id = self.kwargs.get("id", None)
        # get the follow request object by id.
        obj = get_object_or_404(FollowRequest, id=follow_id, receiver=self.request.user.userprofile, status='sent')
        # check object permissions.
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        """
        Decline follow request.
        """  
        follow_request = self.get_object()   
        follow_request.status = 'declined'
        follow_request.save() 
        return Response({'success':"you have declined this follow request successfully."}, status=status.HTTP_200_OK)

        
class UserFollowingListAPIView(generics.ListAPIView):
    """
    Display a list of user's followings.
    """
    serializer_class = UserFollowingSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def get_object(self, *args, **kwargs):
        # get user id from the requested url
        user_id = self.kwargs.get("id", None)
        # get the user profile object by id
        obj = get_object_or_404(UserProfile, id=user_id)
        # check object permissions
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get user followings queryset 
        return self.get_object().following.all()


class UserFollowersListAPIView(generics.ListAPIView):
    """
    Display a list of user's followers.
    """
    serializer_class = UserFollowersTagSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"request":self.request}

    def get_object(self, *args, **kwargs):
        # get user id from the requested url
        user_id = self.kwargs.get("id", None)
        # get the user profile object by id
        obj = get_object_or_404(UserProfile, id=user_id)
        # check object permissions
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get user followers queryset
        return self.get_object().get_followers


class UserItemsListAPIView(generics.ListAPIView):
    """
    Display a list of user's items.
    """
    serializer_class = ItemListSerializer

    def get_object(self, *args, **kwargs):
        # get user id from the requested url
        user_id = self.kwargs.get("id", None)
        # get the user profile object by id
        obj = get_object_or_404(UserProfile, id=user_id)
        # check object permissions
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get user items queryset
        return self.get_object().user.items.all()


class UserItemsFavouritesListAPIView(generics.ListAPIView):
    """
    Display a list of user's favourites items.
    """
    serializer_class = ItemListSerializer

    def get_object(self, *args, **kwargs):
        # get user id from the requested url
        user_id = self.kwargs.get("id", None)
        # get the user profile object by id
        obj = get_object_or_404(UserProfile, id=user_id)
        # check object permissions
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get user items favourites queryset
        return self.get_object().user.favourites.all()


class UserItemsTaggedListAPIView(generics.ListAPIView):
    """
    Display a list of user's tagged items.
    """
    serializer_class = ItemListSerializer

    def get_object(self, *args, **kwargs):
        # get user id from the requested url
        user_id = self.kwargs.get("id", None)
        # get the user profile object by id
        obj = get_object_or_404(UserProfile, id=user_id)
        # check object permissions
        self.check_object_permissions(self.request, obj)
        return obj
        
    def get_queryset(self, *args, **kwargs):
        # get user items tagged queryset
        return self.get_object().tags.all()