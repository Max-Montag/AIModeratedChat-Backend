from django.urls import path
from .views import MessageListCreateView

urlpatterns = [
    path('chatrooms/<str:chatroom_id>/messages/',
         MessageListCreateView.as_view()),
]
