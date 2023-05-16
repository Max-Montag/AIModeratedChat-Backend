from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Message
from .serializers import MessageSerializer


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
