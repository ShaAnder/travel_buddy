"""
Form to create and update recommendations.

This form allows users to create or update a recommendation, including
the title, description, address, categories, and geographic coordinates
(latitude and longitude). It links the form to the `Recommendation` model
and ensures proper population of the `category` field.
"""
from django import forms
from .models import Recommendation, Category


class RecommendationForm(forms.ModelForm):
    """
    Define the Recommendation form.

    This form is used to handle the creation and editing of recommendations.
    It includes fields for the recommendation's title, description, address,
    categories, and geographic coordinates. The category field is populated
    with available categories from the `Category` model.
    """

    class Meta:
        """
        Metadata for the RecommendationForm.

        This inner class defines the model associated with the form
        (`Recommendation`) and the fields to be included in the form,
        such as title, description, address, categories, latitude,
        and longitude.
        """

        model = Recommendation
        fields = [
            "title",
            "description",
            "address",
            "categories",
            "latitude",
            "longitude"
            ]

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Choose a category"
        )
