from django.contrib import admin

from .models import Item, ItemHashtag, ItemTag, ItemLike, ItemFavourite, Comment

class ItemHashtagAdmin(admin.TabularInline):
    """
    Display the item Hashyag model as a tabular inline.
    """
    model = ItemHashtag

class ItemTagAdmin(admin.TabularInline):
    """
    Display the item Tag model as a tabular inline.
    """
    model = ItemTag

class ItemFavouriteAdmin(admin.TabularInline):
    """
    Display the item favourite model as a tabular inline.
    """
    model = ItemFavourite


class ItemLikeAdmin(admin.TabularInline):
    """
    Display the item like model as a tabular inline.
    """
    model = ItemLike

class ItemAdmin(admin.ModelAdmin):
    """
    Override the user profile admin and customize the items display.
    """
    inlines = [ItemHashtagAdmin, ItemTagAdmin, ItemFavouriteAdmin, ItemLikeAdmin]
    # list_display  = []
    # search_fields = []

    class Meta:
        model = Item



# models admin site registeration 
admin.site.register(Item, ItemAdmin)
admin.site.register(Comment)
