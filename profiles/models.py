from django.contrib.auth.models import User
from django.db import models

# user profile model class
# I want there 
class Profile(models.Model):
    # for now they have a default avatar, but could look at an avatar model
    # with extra upload your own / pick from defaults functionality    
    AVATAR_CHOICES = [
        ("images/header-image.webp", "Avatar 1"),
    ]

    #create a user one to one field to the user, ensuring unique profile accounts
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    #bio for user creating a bio
    bio = models.TextField(blank=True)
    #their main location, while they can choose one to visit they have a main one of their own
    location = models.CharField(max_length=100, blank=True)
    #thier avatar they can pick from a variety of profile pics
    avatar = models.CharField(max_length=255, choices=AVATAR_CHOICES, default="images/header-image.webp")

    # details for the admin
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
