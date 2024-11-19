from django.db import models
from user.models import YapsterUser, User

# Create your models here.

# Chat Contains User and Message
class Chat(models.Model):
    chat_name = models.CharField(max_length=255)
    def __str(self):
        return self.chat_name

class ChatUser(models.Model):
    member = models.ForeignKey(YapsterUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat , related_name='chatuser',on_delete=models.CASCADE)
    #ChatUser
    #chatid = 0
    #member = 1

class Message(models.Model):
    
    chat = models.ForeignKey(Chat , on_delete=models.CASCADE, null=True)
    #change to yapster user
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    # temp ra nang null equal true
    content = models.CharField(max_length=5000)
    date_sent = models.DateField(auto_now_add=True)
