from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    """Profile Model

    Args:
        models (Class)

    Description:
        Model containing the db setup for our user profile, when the model is
        builds a databse using the variables below

    Returns:
        __str__ for the admin view that shows the text formatted as such
    """
    AVATAR_CHOICES = [
        ("images/header-image.webp", "Avatar 1"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.CharField(max_length=255, choices=AVATAR_CHOICES, default="images/header-image.webp")

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
