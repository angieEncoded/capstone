from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin # Import this to allow us to adjust the user passwords in the admin module

# Helpful post to configure custom fields in the django admin interface
# https://stackoverflow.com/questions/48011275/custom-user-model-fields-abstractuser-not-showing-in-django-admin/48013640
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Custom Fields',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'role',
                    'title',
                    'department',
                    'extension',
                    'cellphone',
                    'street',
                    'city',
                    'state',
                    'zip',
                    'country',
                ),
            },
        ),
    )



# class AuctionAdmin(admin.ModelAdmin):
#     list_display = ("id", "title", "description", "starting_bid", "url", "high_bid", "category", "listed_by", "winner", "ended")

# class BidAdmin(admin.ModelAdmin):
#     list_display = ("id", "bid_amount", "bidder", "item_id")

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ("id", "item_id", "content", "user")

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "image")

# class WatchlistAdmin(admin.ModelAdmin):
#     list_display = ("id", "item", "user")



# Register your models here.
admin.site.register(User, CustomUserAdmin)
# admin.site.register(Auction, AuctionAdmin)
# admin.site.register(Bid, BidAdmin)
# admin.site.register(Comment, CommentAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Watchlist, WatchlistAdmin)