from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatRoom(models.Model):
    participant1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="participant1")
    participant2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="participant2")


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
