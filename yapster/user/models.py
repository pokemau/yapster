from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class YapsterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='yapsteruser')
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username