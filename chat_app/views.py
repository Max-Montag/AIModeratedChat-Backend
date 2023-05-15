from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(chatroom_id=self.kwargs['chatroom_id'])


class ChatRoomCreateView(ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

    def post(self, request, *args, **kwargs):
        chatroom = ChatRoom.objects.create()
        serializer = self.get_serializer(chatroom)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
