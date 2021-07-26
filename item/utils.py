import random
import string

from django.utils.timesince import timesince

from explore.models import Hashtag
from profiles.models import UserProfile
from notifications.models import Notification


def datetime_to_string(datetime):
    """
    Take a datetime object and return a nicely formatted string, eg: Aug 06, 2020 at 07:21 PM. 
    """
    return datetime.strftime("%b %d, %Y at %I:%M %p")

def rounded_timesince(datetime):
    """
    Take a datetime object and return the time between d and now rounded to lowest integer 
    as a nicely formatted string, eg: 7 hours, 16 minutes will be rounded to be 7 hours.
    """
    return timesince(datetime).split(",")[0]

def random_string_generator(length=10):
    """
    Generate a random alphanumeric string of letters and digits of a given fixed length.
    """
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def unique_slug_generator(instance, new_slug=None):
    """
    Generate a unique slug of given instance.
    """
    # check if the given arguments have a value of new slug
    # if yes, assign the given value to the slug field. 
    if new_slug is not None:
        slug = new_slug
    # if not, generate a slug of a random string.
    else:
        slug = random_string_generator()
    # get the instance class. 
    Klass = instance.__class__
    # check if there's any item with the same slug.
    qs_exists = Klass.objects.filter(slug=slug).exists()
    # if yes, generate a new slug of a random string and return recursive function with the new slug.
    if qs_exists:
        new_slug = random_string_generator()
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def add_hashtags(item_obj, hashtags_lst):
    """
    Take item obj and hashtgas list, convert hashtags to queryset,
    add them to the item. 
    """
    hashtags_qs = Hashtag.objects.hashtag_to_qs(hashtags_lst)
    item_obj.hashtags.set(hashtags_qs)     


def add_tags(item_obj, tags_lst, is_update=False):
    """
    Take item obj and tags list, convert tags to queryset,
    if is update, inactive 
    """
    # convert the submitted tags string to a tags queryset.
    tags_qs = UserProfile.objects.tag_to_qs(tags_lst)
    # add tags to the item's tags.
    item_obj.tags.set(tags_qs)
    # create tag notification for each user. 
    sender = item_obj.owner.userprofile
    if is_update:
        # inactive notifications of tags that are no longer exist.
        Notification.objects.inactive_tag_notification(sender=sender, item=item_obj, notification_type='tag')
        for tag in tags_qs:  
            # set each tag as a notification receiver.
            receiver = tag
            # get tag notification for this item if it already exists, if not, create new one.
            Notification.objects.get_or_create_notification(sender=sender, receiver=receiver, item=item_obj, notification_type='tag')
    else:
        for tag in tags_qs:
            receiver = tag
            Notification.objects.create(sender=sender, receiver=receiver, item=item_obj, notification_type='tag')