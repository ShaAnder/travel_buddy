from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from allauth.account.forms import LoginForm, SignupForm
from django.http import HttpResponse

def profile(request):
    # user = request.User
    # # Access the profile via the `related_name`
    # profile = user.profile 
    # # Get all recommendations made by the user
    # recommendations = user.recommendations.all()  

    return render(request, "profiles/profile.html", {'show_navbar': True})
    # return render(request, "profiles/profile.html", {
    #     "profile": profile,
    #     "recommendations": recommendations,
    # })

# custom allauth views - these overwrite the default views and are different from 
# our django signal, the forms are for creating the account, once the account / user
# is created it then fires our signal which creates a profile. It's from there the
# profile will be checked for updates ect

def login(request):
    # check if posting
    if request.method == 'POST':
        # create and check if form valid
        form = LoginForm(request.POST)
        if form.is_valid():
            # Perform the login
            auth_login(request, form.get_user())
            return redirect('recommendations') 
    else:
        # render our loginform
        form = LoginForm()
    # return our render request
    return render(request, 'account/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create the new user account
            form.save()
            # Optionally, log the user in after signup
            new_user = form.save(commit=False)
            auth_login(request, new_user)
            return redirect('recommendations')
    else:
        form = SignupForm()

    return render(request, 'account/signup.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('recommendations')