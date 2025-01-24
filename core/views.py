from django.shortcuts import render

# we create our view for home page here
def home(request):
    return render(request, "core/home.html", {'show_navbar': False})

# we create our view for home page here
def about(request):
    return render(request, "core/about.html", {'show_navbar': True})

# we create our view for home page here
def policy(request):
    return render(request, "core/policy.html", {'show_navbar': True})