### IMPORTS ###

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from recommendations.models import Recommendation
from django.contrib.auth.decorators import login_required
from allauth.account.forms import LoginForm, SignupForm
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
    user = get_object_or_404(User, username=username)
    profile = user.profile
    recommendations = Recommendation.objects.filter(user=user)
    return render(request, "profiles/profile.html", {
        "profile": profile,
        "recommendations": recommendations,
        "can_edit": request.user == user 
    })

@login_required
def edit_profile(request):
    """Edit Profile View

    Args:
        request (request): request click we recieve from the edit button

    Description:
        the view (or function) that handles loading our edit profile form
    """
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance = profile)
        if form.is_valid():
            form.save()
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {"form": form})

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
            return redirect('recommendations') 
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def signup(request):
    """Signup View

    Args:
        request (_type_): request from the click to signup

    Description:
        custom signup view override for djangos allauth signup view, 
        allows us to sign the user up and add optional extras like auto login ect

    Returns:
        returns the render of our signup page and redirect them to the recommendations
        if they are verified (must click verification email)
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = form.save(commit=False)
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
        custom logout overide, allows user to logout and 
        redirects straight to recommendations

    Returns:
        returns the redirect to recommendations
    """
    auth_logout(request)
    return redirect('recommendations')