"""
Define views for user account and profile management.

This module handles views for displaying and editing user profiles,
deleting user accounts, and logging out users. It includes profile-related
actions such as viewing recommendations, updating profile information,
and handling account deletion with confirmation.
"""
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from recommendations.models import Recommendation
from .import forms

# PROFILE VIEWS #


def profile(request, username):
    """
    Profile view to display user profile along with their recommendations.

    Args:
        request (HttpRequest): The request object to handle the request.
        username (str): The username of the user whose profile is being viewed.

    Returns:
        HttpResponse: Render profile page with the user's details
    """
    user = get_object_or_404(User.objects.select_related('profile'), username=username)
    recommendations = Recommendation.objects.filter(user=user)
    delete_account_url = reverse("delete_account", kwargs={"username": username})
    return render(request, "profiles/profile.html", {
        "profile": user.profile,
        "recommendations": recommendations,
        "can_edit": request.user == user,
        "delete_account_url": delete_account_url,
    })


@login_required
def edit_profile(request, username=None):
    """
    Edit profile view allowing users to update their profile information.

    Args:
        request (HttpRequest): The request object to handle the edit profile request.
        username (str, optional): The username of the profile to edit. Defaults to None.

    Returns:
        HttpResponse: Renders the edit profile page with the profile form.
    """
    if username and request.user.username != username:
        return render(request, "error/403.html", status=403)

    profile = get_object_or_404(User, username=username or request.user.username).profile

    if request.method == "POST":
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
        else:
            messages.error(request, "There were some issues with your submission. Please check the form.")
    else:
        form = forms.ProfileForm(instance=profile)
    return render(request, "profiles/edit_profile.html", {"form": form, "profile": profile})


@login_required
def delete_account(request, username=None):
    """
    View to delete a user's account after confirmation.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Redirects and logs the user out after account deletion.
    """
    if username and request.user.username != username:
        return render(request, "error/403.html", status=403)

    if request.method == "POST":
        password = request.POST.get('password')

        user = authenticate(username=request.user.username, password=password)
        if user is not None:           
            user.profile.delete()
            user.delete()
            messages.success(request, "Your account has been deleted successfully.")
            logout(request)
            return redirect('home')
        else:
            messages.error(request, "Incorrect password. Please try again.")
            return redirect('profile', username=request.user.username)

    return redirect('profile', username=request.user.username)


# ALL AUTH ACCOUNT MANAGEMENT VIEWS #

def logout(request):
    """
    Logout view to log out the current user and redirect to recommendations.

    Args:
        request (HttpRequest): The request object for logging out the user.

    Returns:
        HttpResponse: Redirects the user to the recommendations page after logout.
    """
    auth_logout(request)
    return redirect('home')
