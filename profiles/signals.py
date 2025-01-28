# IMPORTS
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_save_user_profile(sender, instance, created, **kwargs):
    """user profile signal handler

    Args:
        sender (_type_): the model being sent in
        instance (_type_): the instance of the model
        created (_type_): when it was created? (unsure)

    Description:
        Signal for handling user profile instance creation
        when the profile is created it saves a profile instance
        for future use whenever the profile is used / modified
        **Quick Note** sender and kwargs are not nessecarily used here
        however it's good practice to include them
    """
    if created:
        # Create the profile if the user is created
        Profile.objects.create(user=instance)
    else:
        # Save the profile instance for existing users
        instance.profile.save()

