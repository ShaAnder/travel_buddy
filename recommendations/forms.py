from django import forms
from .models import Recommendation, Category

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ["title", "description", "address", "categories", "latitude", "longitude"]

    # You can also explicitly define the category field to ensure it's properly populated
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Choose a category")
