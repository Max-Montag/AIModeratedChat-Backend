from rest_framework import generics, ListCreateAPIView
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(chatroom_id=self.kwargs['chatroom_id'])
    
class ChatRoomCreateView(ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
