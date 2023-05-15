from rest_framework import generics
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializer


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(chatroom_id=self.kwargs['chatroom_id'])

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            author = self.request.user
        else:
            # TODO - remove this default author
            author, _ = User.objects.get_or_create(username='default')
        serializer.save(author=author)
