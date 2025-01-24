from django.shortcuts import render

def recommendations(request):
    return render(request, "recommendations/recommendations.html", {'show_navbar': True})

def add_recommendation(request):
    return render(request, "recommendations/add_recommendation.html", {'show_navbar': True})