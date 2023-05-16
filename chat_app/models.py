from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatRoom(models.Model):
    name = models.CharField(max_length=100, default='testRoom')
    users = models.ManyToManyField(User, related_name='chatrooms')


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)


class Friendship(models.Model):
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user2")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user1', 'user2'),)
