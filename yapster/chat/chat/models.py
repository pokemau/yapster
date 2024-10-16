from django.db import models
from user.models import YapsterUser, User

# Create your models here.
class Chat(models.Model):
    chat_name = models.CharField(max_length=100)
    pass

class ChatUser(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_belong = models.ForeignKey(Chat , on_delete=models.CASCADE)
    #ChatUser
    #chatid = 0
    #member = 1

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    # temp ra nang null equal true
    chat_belong = models.ForeignKey(Chat , on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=5000)
    date_sent = models.DateField(auto_now_add=True)
