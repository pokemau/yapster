from django.db import models
from user.models import YapsterUser

class WordleGame(models.Model):
    creator = models.OneToOneField(YapsterUser, on_delete=models.CASCADE,
                                   related_name='wordle_creator')
    word = models.CharField(max_length=5)
    tries = models.IntegerField(default=1)
