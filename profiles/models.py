from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    """
    Represents a user's profile containing personal information and avatar.

    Args:
        user (OneToOneField): A relationship field linking the profile to a User.
        bio (str): A short biography or description of the user.
        location (str): The user's location.
        avatar (CloudinaryField): An avatar image uploaded to Cloudinary.

    Description:
        This model is used to store user profile information, including the user's 
        bio, location, and avatar. It links to the `User` model with a one-to-one 
        relationship. The `avatar` field uses Cloudinary for image storage.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = CloudinaryField('image', default='avatars/default_avatar.png')

    def __str__(self):
        """
        Returns a string representation of the user's profile.

        Returns:
            str: The username followed by "'s Profile".
        """
        return f"{self.user.username}'s Profile"
