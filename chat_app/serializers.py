from rest_framework import serializers
from .models import ChatRoom, Message, Friendship


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'text', 'chatroom', 'author', 'timestamp']


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'name']


class FriendshipSerializer(serializers.ModelSerializer):
    user1 = serializers.StringRelatedField()
    user2 = serializers.StringRelatedField()

    class Meta:
        model = Friendship
        fields = ['user1', 'user2']
