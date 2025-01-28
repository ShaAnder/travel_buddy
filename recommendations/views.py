from django.shortcuts import render, redirect
from . import forms

def recommendations(request):
    """
    View to return the recommendation page, currently just returns 
    recommendation page will later be used to populate live pings
    of interesting places to visit.
    """
    return render(request, "recommendations/recommendations.html")

def add_recommendation(request):
    """
    Handles the creation of a new recommendation.
    
    Args:
        request: The HTTP request object containing user data and form submission.

    Returns:
        Redirects to the user's profile page after saving the new recommendation.
    
    Description:
        This view renders a form for creating a new recommendation. If the form is valid, 
        it associates the recommendation with the logged-in user and saves it to the database.
    """
    if request.method == 'POST':
        form = forms.RecommendationForm(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.user = request.user  # Associate the recommendation with the logged-in user
            recommendation.save()
            return redirect('profile', username=request.user.username)  # Redirect to the profile page
    else:
        form = forms.RecommendationForm()
    return render(request, 'profiles/add_recommendation.html', {'form': form})