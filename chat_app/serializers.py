from rest_framework import serializers
from .models import ChatRoom, User, UserProfile, Message


class UserProfileSerializer(serializers.ModelSerializer):
    partner = serializers.StringRelatedField()

    class Meta:
        model = UserProfile
        fields = ['partner']


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'userprofile']


class MessageSerializer(serializers.ModelSerializer):
    chatroom = serializers.PrimaryKeyRelatedField(
        queryset=ChatRoom.objects.all(), required=False)
    author = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'text', 'chatroom', 'author', 'timestamp']
