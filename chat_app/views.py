import os
import random
from django.conf import settings
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(chatroom_id=self.kwargs['chatroom_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        if self.request.user.is_authenticated:
            author = self.request.user
        else:
            # TODO - remove this default author
            author, _ = User.objects.get_or_create(username='default')
        serializer.save(author=author)


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(username=username, password=password)

        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)


class UserChatRoomListView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.chatrooms.all()


class ChatRoomCreateView(generics.CreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        adjectives_path = os.path.join(
            settings.BASE_DIR, "wordlist", "adjectives.txt")
        nouns_path = os.path.join(settings.BASE_DIR, "wordlist", "nouns.txt")

        with open(adjectives_path, "r") as file:
            adjectives = file.read().splitlines()
        with open(nouns_path, "r") as file:
            nouns = file.read().splitlines()

        name = f"{random.choice(adjectives)} {random.choice(nouns)}"
        chatroom = ChatRoom.objects.create(name=name)
        chatroom.users.add(request.user)
        chatroom.save()

        serializer = self.get_serializer(chatroom)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
