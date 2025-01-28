from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    """
    Form to handle profile editing.

    Args:
        forms (django.forms.ModelForm): A base class for creating model-based forms.

    Description:
        This form is used to edit a user's profile, allowing them to update
        their bio, location, and avatar. Constraints are added for validation.
    """
    class Meta:
        """
        Metadata for the ProfileForm class.

        Specifies the model to be used (Profile) and the fields that
        should be included in the form (bio, location, avatar).
        """
        model = Profile
        fields = ['bio', 'location', 'avatar']

    def clean_bio(self):
        """
        Validates the bio field to ensure it's not too long.
        Max length constraint is set to 500 characters.
        """
        bio = self.cleaned_data.get('bio')
        if len(bio) > 500:
            raise forms.ValidationError("Bio cannot exceed 500 characters.")
        return bio

    # def clean_avatar(self):
    #     avatar = self.cleaned_data.get('avatar')
    #     if avatar:
    #         # List of allowed avatar file extensions
    #         allowed_extensions = ['.jpg', '.jpeg', '.png', 'webp']
    #         extension = avatar.name.split('.')[-1].lower()
    #         if f".{extension}" not in allowed_extensions:
    #             raise forms.ValidationError("Invalid file type for avatar. Allowed types: .jpg, .jpeg, .png.")
    #     return avatar