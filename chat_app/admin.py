from django.contrib import admin
from .models import ChatRoom, Message, UserProfile

admin.site.register(UserProfile)
admin.site.register(ChatRoom)
admin.site.register(Message)
