from django.contrib import admin
from .models import Event, MarketplaceItem, LostAndFound, RideShare

admin.site.register(Event)
admin.site.register(MarketplaceItem)
admin.site.register(LostAndFound)
admin.site.register(RideShare)
