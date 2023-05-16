from django.urls import path
from .views import ChatRoomCreateView, MessageListCreateView, RegisterView, UserChatRoomListView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('chatrooms/<str:chatroom_id>/messages/',
         MessageListCreateView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('chatrooms/', UserChatRoomListView.as_view(), name='user_chatrooms'),
    path('chatrooms/create/', ChatRoomCreateView.as_view(), name='chatroom_create'),
]
