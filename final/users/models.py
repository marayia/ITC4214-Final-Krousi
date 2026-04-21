from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    bio = models.TextField(blank=True, max_length=150)

    def __str__(self):
        return self.user.username
