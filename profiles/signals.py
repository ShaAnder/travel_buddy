# IMPORTS
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# we want to create a new profile instance if a new user and save if existing
# this is for ease and preventing the user for having to take extra
# steps on signup, they can edit their profile later

# create the profile
@receiver(post_save, sender=User)
def create_save_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create the profile if the user is created
        Profile.objects.create(user=instance)
    else:
        # Save the profile for existing users
        instance.profile.save()
