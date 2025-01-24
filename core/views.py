from django.shortcuts import render

# we create our view for home page here
def home(request):
    return render(request, "core/home.html", {'show_navbar': True})