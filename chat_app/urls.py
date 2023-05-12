from django.urls import path
from .views import MessageListCreateView

urlpatterns = [
    path('api/chatrooms/<int:chatroom_id>/messages/', MessageListCreateView.as_view()),
]