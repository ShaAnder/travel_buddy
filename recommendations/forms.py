from django import forms
from .models import Recommendation

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ["title", "description", "address", "categories"]