from rest_framework import serializers
from .models import ChatRoom, Message, Friendship, User


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'text', 'chatroom', 'author', 'timestamp']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ChatRoomSerializer(serializers.ModelSerializer):
    participant1 = UserSerializer()
    participant2 = UserSerializer()

    class Meta:
        model = ChatRoom
        fields = ['id', 'participant1', 'participant2']


class FriendshipSerializer(serializers.ModelSerializer):
    user1 = UserSerializer()
    user2 = UserSerializer()

    class Meta:
        model = Friendship
        fields = ['user1', 'user2']
