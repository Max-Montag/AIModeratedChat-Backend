from django.urls import path
from .views import MessageListCreateView, ChatRoomCreateView

urlpatterns = [
    path('chatrooms/<str:chatroom_id>/messages/',
         MessageListCreateView.as_view()),
    path('chatrooms/create', ChatRoomCreateView.as_view()),
]
