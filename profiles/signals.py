# IMPORTS
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import logging

# Initialize logger for this module
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create or save a user profile.

    Args:
        sender (Model): The model that triggered the signal (User).
        instance (User): The instance of the model that was saved.
        created (bool): A flag indicating if the instance is newly created.
        **kwargs (dict): Additional keyword arguments (not used here).

    Description:
        This signal is triggered when a User instance is saved. If the user is newly
        created, it creates a corresponding Profile instance. If the user already has
        a profile, it saves the profile instance.
        
        This function uses logging to track profile creation and saving.
    """
    if created:
        logger.info(f"Creating profile for user: {instance.username}")
        Profile.objects.create(user=instance)
    else:
        logger.info(f"Saving profile for user: {instance.username}")
        instance.profile.save()
