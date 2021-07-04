from item.models import Item, Comment
from explore.models import Hashtag
from profiles.models import UserProfile
from notifications.models import Notification
from explore.serializers import HashtagSerializer
from profiles.serializers import UserFollowersTagSerializer
from accounts.serializers import UserSerializer
from .mixins import ItemLikesCommentsCountMixinSerializer, TimestampMixinSerializer

from rest_framework import serializers


class ItemListSerializer(serializers.ModelSerializer, ItemLikesCommentsCountMixinSerializer):
    """
    Item list serializer.
    """
    item_url = serializers.HyperlinkedIdentityField(view_name='item-api:detail', lookup_field='id')

    class Meta:
        model  = Item
        fields = ['image', 'likes_count', 'comments_count', 'item_url']


class ItemFeedListSerializer(serializers.ModelSerializer, ItemLikesCommentsCountMixinSerializer):
    """
    Item feed list serializer.
    """
    owner = UserSerializer(read_only=True)
    hashtags = HashtagSerializer(read_only=True, many=True)
    item_url = serializers.HyperlinkedIdentityField(view_name='item-api:detail', lookup_field='id')

    class Meta:
        model  = Item
        fields = ['owner', 'image', 'likes_count', 'comments_count', 'caption', 'hashtags', 'item_url']

        
class ItemCreateSerializer(serializers.ModelSerializer, TimestampMixinSerializer):
    """
    Item create serializer.
    """
    owner = UserSerializer(read_only=True)
    hashtags = serializers.CharField(required=False)
    tags = serializers.CharField(required=False)
    
    class Meta:
        model  = Item
        fields = ['owner', 'image', 'caption', 'hashtags', 'tags', 'restrict_comment', 'updated_at', 'created_at', 
            'timesince']

    def create(self, validated_data):
        """
        Create and return a new item.
        """
        request = self.context['request']
        owner = request.user
        image = validated_data['image']
        caption = validated_data.get('caption', None)
        hashtags = validated_data.get('hashtags', None)
        tags = validated_data.get('tags', None)
        restrict_comment = validated_data['restrict_comment']
        # create new item with the submitted data.
        new_item = Item.objects.create(owner=owner, image=image, caption=caption, restrict_comment=restrict_comment)
        # if the submitted data has hashtags.  
        if hashtags:
            # convert the submitted hashtags string to a hashtags queryset.
            hashtags_qs = Hashtag.objects.hashtag_to_qs(hashtags)
            # add hashtags to the item's hashtags.
            new_item.hashtags.set(hashtags_qs)
        # if the submitted data has tags.     
        if tags:
            # convert the submitted tags string to a tags queryset.
            tags_qs = UserProfile.objects.tag_to_qs(tags)
            # add tags to the item's tags.
            new_item.tags.set(tags_qs)
            # set the tag notification sender as the item's owner. 
            sender = new_item.owner.userprofile
            for tag in tags_qs:
                # set each tag as a notification receiver.
                receiver = tag
                # create tag notification for this item.
                Notification.objects.create(sender=sender, receiver=receiver, item=new_item, notification_type='tag')  
        return new_item    


class ItemDetailSerializer(serializers.ModelSerializer, ItemLikesCommentsCountMixinSerializer, TimestampMixinSerializer):
    """
    Item detail serializer.
    """
    owner = UserSerializer(read_only=True)
    hashtags = HashtagSerializer(read_only=True, many=True)
    tags = UserFollowersTagSerializer(read_only=True, many=True)
    update_hashtags = serializers.CharField(required=False)
    update_tags = serializers.CharField(required=False)   
    likes_url = serializers.HyperlinkedIdentityField(view_name='item-api:likes', lookup_field='id')
    favourites_url = serializers.HyperlinkedIdentityField(view_name='item-api:favourites', lookup_field='id')
    favourites_count = serializers.SerializerMethodField()
    
    class Meta:
        model  = Item
        fields = ['owner', 'image', 'caption', 'hashtags', 'tags', 'update_hashtags', 'update_tags', 'likes_url', 
            'likes_count', 'favourites_url', 'favourites_count', 'comments_count', 'restrict_comment', 
            'updated_at', 'created_at', 'timesince']
        read_only_fields = ['image']
    
    def __init__(self, *args, **kwargs):
        super(ItemDetailSerializer, self).__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        request = self.context['request']
        hashtags = validated_data.get('update_hashtags', None)
        tags = validated_data.get('update_tags', None)
        # update item
        instance.caption = validated_data.get('caption', None)
        instance.restrict_comment = validated_data['restrict_comment']
        if hashtags:
            # convert the submitted hashtags string to a hashtags queryset.
            hashtags_qs = Hashtag.objects.hashtag_to_qs(hashtags)
            # add hashtags to the item's hashtags.
            instance.hashtags.set(hashtags_qs)
        if tags:    
            # convert the submitted tags string to a tags queryset.
            tags_qs = UserProfile.objects.tag_to_qs(tags)
            # add tags to the item's tags.
            instance.tags.set(tags_qs)
            # set the tag notification sender as the item's owner. 
            sender = instance.owner.userprofile
            # inactive notifications of tags that are no longer exist.
            Notification.objects.inactive_tag_notification(sender=sender, item=instance, notification_type='tag')
            for tag in tags_qs:  
                # set each tag as a notification receiver.
                receiver = tag
                # get tag notification for this item if it already exists, if not, create new one.
                Notification.objects.get_or_create_notification(sender=sender, receiver=receiver, item=instance, notification_type='tag')
        instance.save()
        return instance

    def get_favourites_count(self, obj):
        return obj.favourites.count()


class CommentDetailSerializer(serializers.ModelSerializer, TimestampMixinSerializer):
    """
    Comment detail serializer.
    """
    owner = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model  = Comment
        fields = ["id", "owner", "item", 'likes_count', "content", 'replies', "updated_at", "created_at", "timesince"]
        read_only_fields = ['item']

    def get_replies(self, obj):
        replies = Comment.objects.get_comment_replies(comment_id=obj.id, item_id=obj.item.id)
        if replies:
            return CommentDetailSerializer(replies, many=True, context=self.context).data
        else:
            return None    

    def get_likes_count(self, obj):
        return obj.likes.count()


class CommentReplyDetailSerializer(serializers.ModelSerializer, TimestampMixinSerializer):
    """
    Comment reply detail serializer.
    """
    owner = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model  = Comment
        fields = ["id", "owner", "item", "content", 'likes_count', "updated_at", "created_at", "timesince"]
        read_only_fields = ['item']

    def get_likes_count(self, obj):
        return obj.likes.count()    