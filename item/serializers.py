from rest_framework import serializers

from item.models import Item, Comment
from explore.models import Hashtag
from profiles.models import UserProfile
from notifications.models import Notification
from explore.serializers import HashtagSerializer
from profiles.serializers import UserFollowersTagSerializer
from accounts.serializers import UserSerializer
from .utils import add_hashtags, add_tags
from .mixins import (ItemCommentLikesCountMixinSerializer, ItemLikesCommentsCountMixinSerializer, 
                        TimestampMixinSerializer)


class ItemListSerializer(serializers.ModelSerializer, ItemLikesCommentsCountMixinSerializer):
    """
    Item list serializer.
    """
    class Meta:
        model  = Item
        fields = ['id', 'image', 'likes_count', 'comments_count']


class ItemFeedListSerializer(serializers.ModelSerializer, ItemLikesCommentsCountMixinSerializer):
    """
    Item feed list serializer.
    """
    owner = UserSerializer(read_only=True)
    hashtags = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)

    class Meta:
        model  = Item
        fields = ['id', 'owner', 'image', 'likes_count', 'comments_count', 'caption', 'hashtags']

        
class ItemCreateSerializer(serializers.ModelSerializer, TimestampMixinSerializer):
    """
    Item create serializer.
    """
    owner = UserSerializer(read_only=True)
    hashtags = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    hashtags_names = serializers.ListField(required=False, child=serializers.CharField(), write_only=True)
    tags = UserFollowersTagSerializer(read_only=True, many=True)
    tags_names = serializers.ListField(required=False, child=serializers.CharField(), write_only=True)
    
    class Meta:
        model  = Item
        fields = ['id', 'owner', 'image', 'caption', 'hashtags', 'hashtags_names', 'tags', 'tags_names', 
            'restrict_comment', 'updated_at', 'created_at', 'timesince']

    def create(self, validated_data):
        """
        Create and return a new item.
        """
        request = self.context['request']
        owner = request.user
        image = validated_data['image']
        caption = validated_data.get('caption', None)
        hashtags_names = validated_data.get('hashtags_names', [])
        tags_names = validated_data.get('tags_names', [])
        restrict_comment = validated_data['restrict_comment']
        # create new item with the submitted data.
        new_item = Item.objects.create(owner=owner, image=image, caption=caption, restrict_comment=restrict_comment)  
        if hashtags_names:
            add_hashtags(new_item, hashtags_names)    
        if tags_names:
            add_tags(new_item, tags_names)
        return new_item    


class ItemDetailSerializer(serializers.ModelSerializer, ItemLikesCommentsCountMixinSerializer, 
                            TimestampMixinSerializer):
    """
    Item detail serializer.
    """
    owner = UserSerializer(read_only=True)
    hashtags = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    tags = UserFollowersTagSerializer(read_only=True, many=True)
    hashtags_names = serializers.ListField(required=False, child=serializers.CharField(), write_only=True)
    tags_names = serializers.ListField(required=False, child=serializers.CharField(), write_only=True)   
    favourites_count = serializers.SerializerMethodField()
    
    class Meta:
        model  = Item
        fields = ['id', 'slug', 'owner', 'image', 'caption', 'hashtags', 'tags', 'hashtags_names', 
            'tags_names', 'likes_count', 'favourites_count', 'comments_count', 'restrict_comment', 
            'updated_at', 'created_at', 'timesince']
        read_only_fields = ['image']
    
    def __init__(self, *args, **kwargs):
        super(ItemDetailSerializer, self).__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        hashtags = validated_data.get('hashtags_names', [])
        tags = validated_data.get('tags_names', [])
        # update item
        instance.caption = validated_data.get('caption', None)
        instance.restrict_comment = validated_data['restrict_comment']
        if hashtags:
            add_hashtags(instance, hashtags)
        if tags:
            add_tags(instance, tags, is_update=True)
        instance.save()
        return instance

    def get_favourites_count(self, obj):
        return obj.favourites.count()


class CommentDetailSerializer(serializers.ModelSerializer, ItemCommentLikesCountMixinSerializer, 
                                TimestampMixinSerializer):
    """
    Comment detail serializer.
    """
    owner = UserSerializer(read_only=True)
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


class CommentReplyDetailSerializer(serializers.ModelSerializer, ItemCommentLikesCountMixinSerializer, TimestampMixinSerializer):
    """
    Comment reply detail serializer.
    """
    owner = UserSerializer(read_only=True)

    class Meta:
        model  = Comment
        fields = ["id", "owner", "item", "content", 'likes_count', "updated_at", "created_at", "timesince"]
        read_only_fields = ['item']   