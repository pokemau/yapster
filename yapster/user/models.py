from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class YapsterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='yapsteruser')
    # birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    # cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.user.username

