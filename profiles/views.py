### IMPORTS ###

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from allauth.account.forms import LoginForm, SignupForm
from recommendations.models import Recommendation
from .forms import ProfileForm

### PROFILE VIEWS ###

def profile(request, username):
    """Profile view

    Args:
        request (request): the request (click) to take us to desired profile
        username (User): the username of the owner of said profile

    Description:
        the view that handles loading the user profile

    Returns:
        returns the render of the template with the args passed in
        the main one to know is that we're passing in the ability to edit
        if the current user is the owner.
    """
    user = get_object_or_404(User.objects.select_related('profile'), username=username)
    recommendations = Recommendation.objects.filter(user=user)
    return render(request, "profiles/profile.html", {
        "profile": user.profile,
        "recommendations": recommendations,
        "can_edit": request.user == user 
    })

@login_required
def edit_profile(request, username=None):
    """Edit Profile View

    Args:
        request (request): request click we receive from the edit button
        username (str): the username being passed into the edit function
        to check current user and allow editing the page

    Description:
        the view (or function) that handles loading our edit profile form
        also has built-in safeguards to prevent editing other users profiles
    """
    if username and request.user.username != username:
        messages.error(request, "You don't have authorization to view this page.")
        return render(request, "profiles/edit_profile.html", {})
    
    profile = get_object_or_404(User, username=username or request.user.username).profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("profile", username=request.user.username)
        else:
            messages.error(request, "There were some issues with your submission. Please check the form.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profiles/edit_profile.html", {"form": form, "profile": profile})

### ALL AUTH ACCOUNT MANAGEMENT VIEWS ###

def login(request):
    """Login View

    Args:
        request (_type_): request from the click to login

    Description:
        custom login view override for djangos allauth login view, 
        allows us to login the user or redirect them to where we want
        them to go

    Returns:
        returns the render of our login page or if logged in returns
        a url redirect to the recommendations page
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
    """Signup View

    Args:
        request (_type_): request from the click to signup

    Description:
        custom signup view override for djangos allauth signup view, 
        allows us to sign the user up and add optional extras like auto login etc

    Returns:
        returns the render of our signup page and redirect them to the recommendations
        if they are verified (must click verification email)
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
    """Logout View

    Args:
        request (_type_): request from the click to logout

    Description:
        custom logout override, allows user to logout and 
        redirects straight to recommendations

    Returns:
        returns the redirect to recommendations
    """
    auth_logout(request)
    return redirect('recommendations')
