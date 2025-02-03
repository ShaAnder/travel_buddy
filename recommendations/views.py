"""
Module for handling recommendation views and API endpoints.

This module contains views to handle the creation, editing, and deletion of
recommendations, as well as viewsets for interacting with the recommendations
and categories through an API.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets
from .serializers import *
from . import models
from . import forms
from . import utils
from travel_buddy.settings import GOOGLE_API


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for the Recommendation model.

    Provides read-only access to the list of recommendations through the API.
    """

    queryset = models.Recommendation.objects.all()
    serializer_class = RecommendationSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for the Category model.

    Provides read-only access to the list of categories through the API.
    """

    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer


def recommendations(request):
    """
    Display the recommendations page.

    Fetches a list of Irish cities and renders the recommendations page.
    This will later be used to populate live suggestions of interesting
    places to visit.

    Args:
        request: The HTTP request object containing user data.

    Returns:
        Rendered HTML response for the recommendations page.
    """
    cities = utils.get_irish_cities()
    return render(request, "recommendations/recommendations.html", {"cities": cities, "google_maps_api_key": GOOGLE_API})


def add_recommendation(request):
    """
    Handle the creation of a new recommendation.

    This view processes a form submission to create a new recommendation. If
    the form is valid, it geocodes the address to get latitude and longitude
    coordinates, then associates the recommendation with the logged-in user
    and saves it to the database.

    Args:
        request: The HTTP request object containing user data and form submission.

    Returns:
        Redirects to the user's profile page after saving the new recommendation.
    """
    if request.method == 'POST':
        form = forms.RecommendationForm(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            address = recommendation.address
            lat, lng = utils.get_lat_long(address)
            if lat is not None and lng is not None:
                recommendation.latitude = lat
                recommendation.longitude = lng
                recommendation.user = request.user
                recommendation.save()
                return redirect('profile', username=request.user.username)
            else:
                # Handle the case where lat/lng is None (API issue)
                print("no lat/lng")
                form.add_error('address', 'Unable to get latitude and longitude.')
    else:
        form = forms.RecommendationForm()

    return render(request, 'recommendations/add_recommendation.html', {'form': form})


def edit_recommendation(request, recommendation_id):
    """
    Handle the editing of an existing recommendation.

    Allows the logged-in user to update their recommendation. If the address
    is changed, it will update the latitude and longitude by geocoding the new
    address.

    Args:
        request: The HTTP request object.
        recommendation_id: The ID of the recommendation being edited.

    Returns:
        A rendered template to edit the recommendation, or a redirect to the user's profile on success.
    """
    recommendation = get_object_or_404(models.Recommendation, id=recommendation_id)

    # Ensure that the logged-in user is the owner of the recommendation
    if recommendation.user != request.user:
        return render(request, "error/403.html", status=403)

    if request.method == 'POST':
        form = forms.RecommendationForm(request.POST, instance=recommendation)
        old_address = recommendation.address
        if form.is_valid():
            updated_recommendation = form.save(commit=False)
            updated_address = updated_recommendation.address
            if updated_address != old_address:
                print(f"Address changed: {updated_address} != {old_address}")
                address = updated_recommendation.address
                lat, lng = utils.get_lat_long(address)
                if lat is not None and lng is not None:
                    updated_recommendation.latitude = lat
                    updated_recommendation.longitude = lng
                    print(f"Updated lat/lng: {lat}, {lng}")
                else:
                    print("Geocoding failed. Address not found.")
                    form.add_error('address', 'Unable to get latitude and longitude.')
            else:
                print("Address not changed, keeping old latitude and longitude.")
            updated_recommendation.save()
            print(f"Recommendation saved: {updated_recommendation.latitude}, {updated_recommendation.longitude}")
            return redirect('profile', username=request.user.username)

    else:
        form = forms.RecommendationForm(instance=recommendation)

    return render(request, 'recommendations/edit_recommendation.html', {'form': form, 'recommendation': recommendation})


def delete_recommendation(request, recommendation_id):
    """
    Handle the deletion of an existing recommendation.

    Allows the logged-in user to delete their own recommendation. If the user
    is not the owner of the recommendation, they are redirected to their
    profile page.

    Args:
        request: The HTTP request object containing user data.
        recommendation_id (int): The ID of the recommendation to be deleted.

    Returns:
        Redirects to the user's profile page after the recommendation is deleted.
    """
    recommendation = get_object_or_404(models.Recommendation, id=recommendation_id)
    # Defensive programming to prevent unauthorized deletion of recommendations
    if recommendation.user != request.user:
        return render(request, "error/403.html", status=403)

    recommendation.delete()
    messages.success(request, "Recommendation deleted successfully!")
    return redirect('profile', username=request.user.username)
