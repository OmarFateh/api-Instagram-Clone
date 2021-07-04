from django.db import models
from django.urls import reverse
from django.db.models import Q, Count
from django.contrib.auth.models import User


def item_image(instance, filename):
    """
    Upload the item image into the path and return the uploaded image path.
    """
    path = f'users/{instance.owner}/{filename}'
    return path


class BaseTimestamp(models.Model):
    """
    Timestamp abstract model.
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


class ItemAbstractRelationship(models.Model):
    """
    A abstract relationship model to inherit from.
    """
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ItemHashtag(ItemAbstractRelationship):
    """
    A relationship model between the item and its hashtags.
    """
    hashtag = models.ForeignKey('explore.Hashtag', on_delete=models.CASCADE)


class ItemTag(ItemAbstractRelationship):
    """
    A relationship model between the item and its tags.
    """
    owner = models.ForeignKey('profiles.UserProfile', on_delete=models.CASCADE)


class ItemLike(ItemAbstractRelationship):
    """
    A relationship model between the item and its likes.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class ItemFavourite(ItemAbstractRelationship):
    """
    A relationship model between the item and its favourites.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
 

class ItemQuerySet(models.QuerySet):
    """
    Override the item queryset.
    """
    def feed(self, user):
        """
        Take a user object and return queryset of items of the requested user and his followings,
        orderd by the latest created ones.
        """
        user_profile = user
        # check if the user has following.
        profiles_exist = user_profile.following.exists()
        followed_users_id = []
        if profiles_exist:
            # get list of all user's following ids.
            followed_users_id = user_profile.following.values_list("userprofile__id", flat=True) 
        # return a queryset of items of user and his following ordered by the latest created ones.    
        return self.filter(
            Q(owner__id__in=followed_users_id)|
            Q(owner=user_profile.user)
        ).distinct().order_by('-created_at')

    def available_items(self, user):
        """
        Take user, and get a queryset of items of user and his following, and those oof non-private accounts.
        """
        user_profile = user
        # check if the user has following.
        profiles_exist = user_profile.following.exists()
        followed_users_id = []
        if profiles_exist:
            # get list of all user's following ids.
            followed_users_id = user_profile.following.values_list("userprofile__id", flat=True) 
        # return a queryset of items of user and his following, and those oof non-private accounts.
        return self.filter(
            Q(owner__id__in=followed_users_id)|
            Q(owner__userprofile__private_account=False)|
            Q(owner=user_profile.user)
        ).distinct()

    def trending(self, user):
        """
        Take user, and get trending items, items with most likes in descending order.
        """
        return self.available_items(user).annotate(like_count=Count('likes')).order_by('-like_count')
    
    def explore(self, user):
        """
        Take user, and get all item of other users whose profiles are not privat, and not in user's following list,
        ordered by latest created ones.
        """
        user_profile = user
        return self.available_items(user_profile).exclude(owner=user_profile.user).order_by('-created_at')


class ItemManager(models.Manager):
    """
    Override the item manager.
    """
    def get_queryset(self, *args, **kwargs):
        """
        Get the item queryset.
        """
        return ItemQuerySet(self.model, using=self._db)

    def feed(self, user):
        """
        Add feed method to the item manager.
        Take a user and return his items and all items of his following.
        """
        return self.get_queryset().feed(user)

    def trending(self, user):
        """
        Add trending method to the item manager.
        Take a user and return trending items.
        """
        return self.get_queryset().trending(user)  

    def explore(self, user):
        """
        Add explore method to the item manager.
        Take a user and return explore items.
        """   
        return self.get_queryset().explore(user)      


class Item(BaseTimestamp):
    """
    Item model.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    image = models.ImageField(upload_to=item_image)
    slug = models.CharField(max_length=10, unique=True, null=True, blank=True)
    caption = models.CharField(max_length=255, null=True, blank=True)
    hashtags = models.ManyToManyField('explore.Hashtag', related_name='item_hashtags', blank=True, through=ItemHashtag)
    tags = models.ManyToManyField('profiles.UserProfile', related_name='tags', blank=True, through=ItemTag)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, through=ItemLike)
    favourites = models.ManyToManyField(User, related_name='favourites', blank=True, through=ItemFavourite)
    restrict_comment = models.BooleanField(default=False)

    objects = ItemManager()
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['-created_at']

    def __str__(self):
        # Return item id and owner.
        return f"{self.id} | {str(self.owner)}" 
  
    def parent_comments(self):
        # Return all parent comments of an item.
        qs = Comment.objects.filter_by_parent(self) 
        return qs       
        

class CommentLike(BaseTimestamp):
    """
    A relationship model between the comment and its likes.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('Comment', on_delete=models.CASCADE)


class CommentManager(models.Manager):
    """
    Override the comment manager.
    """
    def filter_by_parent(self, item):
        """
        Take item, and filter the comment queryset by parent comments.
        """
        qs = super(CommentManager, self).filter(item=item, reply=None)
        return qs

    def get_comment_replies(self, comment_id, item_id):
        """
        Take comment's id and item's id.
        Get replies of this comment for this item.
        """
        return self.get_queryset().filter(id=comment_id, item__id=item_id).first().replies.all()


class Comment(BaseTimestamp):
    """
    Item comment model.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments') # item.comments.all  comment.item.id
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True, through=CommentLike)
    content = models.TextField()

    objects = CommentManager() 
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']

    def __str__(self):
        # Return comment item and owner.
        return f"{self.item} | {str(self.owner)}"

    def parent_comments(self):
        # Return all parent comments of an item.
        qs = Comment.objects.filter_by_parent(self.item) 
        return qs     