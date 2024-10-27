from django.contrib import admin

from .models import FriendList, FriendRequest

admin.site.register(FriendList)
admin.site.register(FriendRequest)