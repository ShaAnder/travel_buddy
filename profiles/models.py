from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    """
    Displays the user's profile page along with their recommendations.
    
    Args:
        request: The HTTP request object containing user data.
        username (str): The username of the user whose profile is being viewed.
    
    Returns:
        Renders the user's profile page with a list of their recommendations.
    
    Description:
        This view fetches the user profile based on the provided username and displays
        the recommendations associated with that user. The recommendations are filtered 
        by the user who created them.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = CloudinaryField('image', default='avatars/default_avatar.png')

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
