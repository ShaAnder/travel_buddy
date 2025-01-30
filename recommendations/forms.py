from django import forms
from .models import Recommendation

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ["title", "description", "address", "categories", "latitude", "longitude"]
        # we want these inputs but we want them hidden so that they ar populated by the function
        widgets = {
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
        }