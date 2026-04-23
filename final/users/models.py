from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    bio = models.TextField(blank=True, max_length=150)

    HEADER_COLORS = [
    ('#344657', 'Forest'),
    ('#79ae6f', 'Sage'),
    ('#4a6fa5', 'Ocean'),
    ('#7b4f8e', 'Dusk'),
    ('#8b5e3c', 'Chestnut'),
    ('#c0545a', 'Berry'),
]
    header_color = models.CharField(max_length=7, choices=HEADER_COLORS, default='#344657')
    
    def __str__(self):
        return self.user.username
