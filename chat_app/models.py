from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(max_length=100, default='testRoom')


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    text = models.TextField()
