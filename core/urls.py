"""
Define URL patterns for the Core application.

This module specifies the URL configurations for the Core app, mapping
routes to their corresponding view functions.
"""
from django.urls import path
from .views import home, about
# url patterns for core features
urlpatterns = [
    path("", home, name="home"),
    path("home/", home, name="home"),
    path("about/", about, name="about"),
]
