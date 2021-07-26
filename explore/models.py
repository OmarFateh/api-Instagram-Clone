from django.db import models
from django.urls import reverse
            
from .utils import arabic_slugify


class HashtagManager(models.Manager):
    """
    Override the hashtag manager.
    """
    def created_or_new(self, title):
        """
        Take a title of a hashtag, and get it if it's already exist, and if not, create a new one. 
        """
        title = title.strip()
        # get queryset of all hashtags with that title.
        qs = self.get_queryset().filter(name__iexact=title)
        # if hashtags exist.
        if qs.exists():
            # get the first hashtag of the queryset.
            return qs.first(), False
        # if not, create new hashtag.   
        return Hashtag.objects.create(name=title), True

    def hashtag_to_qs(self, hashtags_list):
        """
        Take a string of hashtags, and return a queryset of hashtags.  
        """
        hashtags_ids = []
        for hashtag in hashtags_list:
            # get or create each hashtag by using created_or_new method.
            obj, created = self.created_or_new(hashtag)
            hashtags_ids.append(obj.id) 
        # get queryset of hashtags by filtering their ids.
        return self.get_queryset().filter(id__in=hashtags_ids).distinct()
    

class Hashtag(models.Model):
    """
    Hashtag model.
    """
    name = models.CharField(max_length=256, verbose_name='hashtag')
    slug = models.SlugField(unique=True, allow_unicode=True, null=True, blank=True)

    objects = HashtagManager()

    class Meta:
        verbose_name = 'Hashtag'
        verbose_name_plural = 'Hashtags'

    def __str__(self):
        # Return hashtag's title.
        return self.name   

    def save(self, *args, **kwargs):
        # Override the save method and slugify the hashtag name before saving. 
        if not self.slug:
            self.slug = arabic_slugify(self.name)
        super(Hashtag, self).save(*args, **kwargs)