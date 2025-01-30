from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . import models
from . import forms
from core.utils import get_lat_long
from travel_buddy.settings import OPENCAGE_API


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
            address = recommendation.address
            lat, lng = get_lat_long(address, OPENCAGE_API)
            if lat is not None and lng is not None:
                recommendation.latitude = lat
                recommendation.longitude = lng
                recommendation.user = request.user
                recommendation.save()
                return redirect('profile', username=request.user.username)
            else:
                # Handle the case where lat/lng is None (API issue)
                print("no lat/lng")
                form.add_error('address', 'Unable to get latitude and longitude.')
    else:
        form = forms.RecommendationForm()

    return render(request, 'recommendations/add_recommendation.html', {'form': form})


def edit_recommendation(request, recommendation_id):
    """
    Handles the editing of an existing recommendation.
    
    Args:
        request: The HTTP request object containing user data and form submission.
        recommendation_id (int): The ID of the recommendation to be edited.
    
    Returns:
        Redirects to the user's profile page after saving the updated recommendation.
    
    Description:
        This view allows the logged-in user to edit their own recommendation. 
        If the user is not the owner of the recommendation, they are redirected 
        to their profile page.
    """
    recommendation = get_object_or_404(models.Recommendation, id=recommendation_id)
    if recommendation.user != request.user:
        return render(request, "error/403.html", status=403)
    if request.method == 'POST':
        form = forms.RecommendationForm(request.POST, instance=recommendation)
        if form.is_valid():
            updated_recommendation = form.save(commit=False)
            #bug it thinks that even when we change address it's the same address
            #but functionality still works the same
            if updated_recommendation.address == recommendation.address:
                address = updated_recommendation.address
                lat, lng = get_lat_long(address, OPENCAGE_API)
                updated_recommendation.lat = lat
                updated_recommendation.lng = lng
            else:
                # Handle the case where lat/lng is None (API issue)
                print("no lat/lng")
                form.add_error('address', 'Unable to get latitude and longitude.')
            updated_recommendation.save()
            return redirect('profile', username=request.user.username)
    else:
        form = forms.RecommendationForm(instance=recommendation)

    return render(request, 'recommendations/edit_recommendation.html', {'form': form, 'recommendation': recommendation})


def delete_recommendation(request, recommendation_id):
    """
    Handles the deletion of an existing recommendation.
    
    Args:
        request: The HTTP request object containing user data.
        recommendation_id (int): The ID of the recommendation to be deleted.
    
    Returns:
        Redirects to the user's profile page after the recommendation is deleted.
    
    Description:
        This view allows the logged-in user to delete their own recommendation. 
        If the user is not the owner of the recommendation, they are redirected 
        to their profile page.
    """
    recommendation = get_object_or_404(models.Recommendation, id=recommendation_id)
    #defensive programming stop user from navigating via url to delete others recommendation
    print(id)
    if recommendation.user != request.user:
        return render(request, "error/403.html", status=403)
    
    recommendation.delete()
    messages.success(request, "Recommendation deleted successfully!")
    return redirect('profile', username=request.user.username)