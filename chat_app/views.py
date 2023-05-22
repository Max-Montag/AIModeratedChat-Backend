from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, Message, UserProfile
from django.db.models import Q
from .serializers import UserSerializer, MessageSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.db import transaction
from .bot import create_bot_message


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.set_cookie('access_token', response.data['access'],
                            httponly=False, samesite='Lax')
        response.set_cookie('refresh_token', response.data['refresh'],
                            httponly=False, samesite='Lax')
        return response


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

        UserProfile.objects.create(user=user)

        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)


class ConnectPartnerView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, user_id):
        print("TRYING TO CONNECT PARTNER"+user_id)
        try:
            partner = User.objects.get(id=user_id)

            if partner == request.user:
                return Response(
                    {"error": "You cannot add yourself as a partner"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if (hasattr(request.user.userprofile, 'partner') and request.user.userprofile.partner is not None) or (hasattr(partner.userprofile, 'partner') and partner.userprofile.partner is not None):
                return Response(
                    {"error": "User or partner already has a partner"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request.user.userprofile.partner = partner
            request.user.userprofile.save()

            partner.userprofile.partner = request.user
            partner.userprofile.save()

            ChatRoom.objects.create(
                participant1=request.user, participant2=partner)

            return Response({"message": "Partner connected and chatroom created"}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class PartnerDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        partner = user.userprofile.partner

        if partner is None:
            raise Response({"error": "No partner connected"},
                           status=status.HTTP_404_NOT_FOUND)

        return partner


class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        partner = user.userprofile.partner

        if partner is None:
            return

        try:
            chatroom = ChatRoom.objects.get(
                Q(participant1=user, participant2=partner) |
                Q(participant1=partner, participant2=user)
            )
        except ChatRoom.DoesNotExist:
            return

        return Message.objects.filter(chatroom=chatroom)

    def perform_create(self, serializer):
        user = self.request.user
        partner = user.userprofile.partner

        if partner is None:
            raise Response({"error": "No partner connected"},
                           status=status.HTTP_404_NOT_FOUND)
        try:
            chatroom = ChatRoom.objects.get(
                Q(participant1=user, participant2=partner) |
                Q(participant1=partner, participant2=user)
            )
        except ChatRoom.DoesNotExist:
            return

        serializer.save(chatroom=chatroom, author=self.request.user)

        create_bot_message(chatroom)
