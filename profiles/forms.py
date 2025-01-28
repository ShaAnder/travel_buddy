from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    """
    Form to handle profile editing.

    Args:
        forms (django.forms.ModelForm): A base class for creating model-based forms.

    Description:
        This form is used to edit a user's profile, allowing them to update
        their bio, location, and avatar.
    """
    class Meta:
        """
        Metadata for the ProfileForm class.

        Specifies the model to be used (Profile) and the fields that
        should be included in the form (bio, location, avatar).
        """
        model = Profile
        fields = ['bio', 'location', 'avatar']