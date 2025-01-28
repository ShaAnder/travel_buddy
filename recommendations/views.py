from django.shortcuts import render

def recommendations(request):
    return render(request, "recommendations/recommendations.html")

def add_recommendation(request):
    return render(request, "recommendations/add_recommendation.html")