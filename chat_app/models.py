from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    partner = models.OneToOneField(
        User, related_name='partner_of', null=True, blank=True, on_delete=models.SET_NULL)


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
    processed_by_ai = models.IntegerField(default=0)
