from django.urls import path
from .views import MessageListCreateView, ChatRoomCreateView

urlpatterns = [
    path('api/chatrooms/<int:chatroom_id>/messages/',
         MessageListCreateView.as_view()),
    path('api/chatrooms/create', ChatRoomCreateView.as_view()),
]
