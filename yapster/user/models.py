from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class YapsterUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birthdate = models.DateField('birthdate',null=True)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username
    
class Message(models.Model):
    pass