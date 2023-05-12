from django.db import models

class ChatRoom(models.Model):
    pass

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    text = models.TextField()
