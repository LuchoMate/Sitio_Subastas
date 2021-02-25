from django.contrib import admin
from .models import User, auction_listing, bids, comments

# Register your models here.

admin.site.register(User)
admin.site.register(auction_listing)
admin.site.register(bids)
admin.site.register(comments)
