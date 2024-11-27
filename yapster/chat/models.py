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
    nickname = models.CharField(max_length=255)
    #ChatUser
    #chatid = 0
    #member = 1
    def save(self, *args, **kwargs):
        if not self.nickname and self.member:
            first_name = self.member.user.first_name or ""
            last_name = self.member.user.last_name or ""
            self.nickname = f"{first_name} {last_name}".strip()
        super().save(*args, **kwargs)

class Message(models.Model):
    
    chat = models.ForeignKey(Chat , on_delete=models.CASCADE, null=True)
    #change to yapster user
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    # temp ra nang null equal true
    content = models.CharField(max_length=5000)
    date_sent = models.DateField(auto_now_add=True)
