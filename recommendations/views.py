from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from . import models
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
    #if post
    if request.method == 'POST':
        #set our rec form
        form = forms.RecommendationForm(request.POST)
        #if valid = make the rec
        if form.is_valid():
            #save the form
            recommendation = form.save(commit=False)
            #associate the rec to the user
            recommendation.user = request.user
            #save rec
            recommendation.save()
            #redirect to user profile
            return redirect('profile', username=request.user.username)
    else:
        #else form not valid
        form = forms.RecommendationForm()
    #return rec page + form
    return render(request, 'profiles/add_recommendation.html', {'form': form})


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
    #get rec for comparison
    recommendation = get_object_or_404(models.Recommendation, id=recommendation_id)
    #compare rec user vs current user
    if recommendation.user != request.user:
        #if not current user redirect to owner profile + err msg
        messages.error(request, "You don't have authorization to edit this recommendation.")
        return redirect("profile", username=recommendation.user.username)
    #if owner
    if request.method == 'POST':
        #set form
        form = forms.RecommendationForm(request.POST, instance=recommendation)
        #if valid
        if form.is_valid():
            #save form redirect to profile
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        #display form
        form = forms.RecommendationForm(instance=recommendation)
    #render form / rec
    return render(request, 'profiles/edit_recommendation.html', {'form': form, 'recommendation': recommendation})


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

    if recommendation.user != request.user:
        messages.error(request, "You don't have authorization to edit this recommendation.")
        return redirect("profile", username=recommendation.user.username)
    
    recommendation.delete()
    messages.success(request, "Recommendation deleted successfully!")
    return redirect('profile', username=request.user.username)