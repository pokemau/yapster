from django.db import models
from user.models import YapsterUser
from chat.models import Chat

class WordleGame(models.Model):
    creator = models.ForeignKey(YapsterUser, on_delete=models.CASCADE,
                                   related_name='wordle_creator')
    chatroom = models.ForeignKey(Chat, on_delete=models.CASCADE,
                                    related_name='wordle_chatroom', null=True)
    guesses = models.CharField(max_length=35, null=True)
    word = models.CharField(max_length=5)
    tries = models.IntegerField(default=0)
    solved = models.BooleanField(default=False)
