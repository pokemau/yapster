from django.db import models
from user.models import YapsterUser

class WordleGame(models.Model):
    creator = models.ForeignKey(YapsterUser, on_delete=models.CASCADE,
                                   related_name='wordle_creator')
    receiver = models.ForeignKey(YapsterUser, on_delete=models.CASCADE,
                                    related_name='wordle_receiver', null=True)
    word = models.CharField(max_length=5)
    tries = models.IntegerField(default=0)
