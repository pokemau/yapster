from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(ChatUser)