# IMPORTS #
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from allauth.account.forms import LoginForm, SignupForm
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
        HttpResponse: Renders the profile page with the user's profile and recommendations.
    """
    user = get_object_or_404(User.objects.select_related('profile'), username=username)
  
    recommendations = Recommendation.objects.filter(user=user)
    # Generate a dynamic delete URL for each recommendation
    delete_recommendation_urls = {
        recommendation.id: reverse('delete_recommendation', kwargs={'recommendation_id': recommendation.id})
        for recommendation in recommendations
    }
    delete_account_url = reverse("delete_account", kwargs={"username": username})
    return render(request, "profiles/profile.html", {
        "profile": user.profile,
        "recommendations": recommendations,
        "can_edit": request.user == user,
        "delete_account_url": delete_account_url,
        "delete_recommendation_urls": delete_recommendation_urls,
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
        HttpResponse: Redirects to a confirmation page or logs the user out after account deletion.
    """
    if username and request.user.username != username:
        return render(request, "error/403.html", status=403)

    if request.method == "POST":
        password = request.POST.get('password')

        # Authenticate the user with the provided password
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            # Password is correct, proceed with deletion
            user.profile.delete()  # Optional: delete user profile first
            user.delete()  # Delete the user account
            messages.success(request, "Your account has been deleted successfully.")
            logout(request)  # Log out the user after account deletion
            return redirect('home')  # Redirect to the home page or wherever you want
        else:
            messages.error(request, "Incorrect password. Please try again.")
            return redirect('profile', username=request.user.username)  # Redirect back to the profile page

    return redirect('profile', username=request.user.username)


# ALL AUTH ACCOUNT MANAGEMENT VIEWS #


def login(request):
    """
    Login view for user authentication.

    Args:
        request (HttpRequest): The request object for logging the user in.

    Returns:
        HttpResponse: Renders the login page or redirects to the next page after login.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_url = request.GET.get('next', 'recommendations')  # Redirect to 'next' if it exists
            return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


def signup(request):
    """
    Signup view for creating a new user.

    Args:
        request (HttpRequest): The request object for signing up a new user.

    Returns:
        HttpResponse: Renders the signup page or redirects to recommendations after signup.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            auth_login(request, new_user)
            return redirect('recommendations')
    else:
        form = SignupForm()

    return render(request, 'account/signup.html', {'form': form})


def logout(request):
    """
    Logout view to log out the current user and redirect to recommendations.

    Args:
        request (HttpRequest): The request object for logging out the user.

    Returns:
        HttpResponse: Redirects the user to the recommendations page after logout.
    """
    auth_logout(request)
    return redirect('recommendations')
