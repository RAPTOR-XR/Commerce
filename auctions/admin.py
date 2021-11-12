from django.contrib import admin
from .models import User, AuctionList, AuctionBid, AuctionComment

# Register your models here.
admin.site.register(User)
admin.site.register(AuctionList)
admin.site.register(AuctionBid)
admin.site.register(AuctionComment)