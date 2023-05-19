from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, Message, Friendship
from django.db.models import Q
from .serializers import ChatRoomSerializer, FriendshipSerializer, MessageSerializer, UserSerializer
from .bot import create_bot_message


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(chatroom_id=self.kwargs['chatroom_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

        create_bot_message(self.kwargs['chatroom_id'])


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
        user = self.request.user
        return ChatRoom.objects.filter(Q(participant1=user) | Q(participant2=user))


class ChatRoomCreateView(generics.CreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        invited_user_id = request.data.get('user_id')
        if not invited_user_id:
            return Response({"detail": "Missing user_id field."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            invited_user = User.objects.get(id=invited_user_id)
        except User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

        try:
            chatroom = ChatRoom.objects.get(
                Q(participant1=request.user, participant2=invited_user) |
                Q(participant1=invited_user, participant2=request.user)
            )
            created = False
        except ChatRoom.DoesNotExist:
            chatroom = ChatRoom.objects.create(
                participant1=request.user, participant2=invited_user
            )
            created = True

        serializer = self.get_serializer(chatroom)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK, headers=headers)


class UserFriendsListView(generics.ListAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(user1=user) | Friendship.objects.filter(user2=user)


class AddFriendView(APIView):
    def post(self, request):
        username = request.data.get("username")

        if not username:
            return Response(
                {"error": "Username required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            friend = User.objects.get(username__iexact=username)

            if friend == request.user:
                return Response(
                    {"error": "You cannot add yourself as a friend"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Friendship.objects.create(user1=request.user, user2=friend)

            return Response({"message": "Friend added"}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search = self.request.query_params.get('search', '')
        queryset = User.objects.filter(Q(username__icontains=search))
        return queryset
