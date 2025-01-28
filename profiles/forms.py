from django import forms
from .models import Profile

# we want to create a form to handle our profile editing
class ProfileForm(forms.ModelForm):
    """
    Profile Form

    Args:
        forms (django class)

    Description:
        Creates a form based on the meta date below
    """
    class Meta:
        # basic form setup
        model = Profile
        fields = ['bio', 'location', 'avatar']