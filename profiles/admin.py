"""
Register Profile model with the Django admin site.

This module registers the Profile model, allowing it to be managed
through the Django admin interface.
"""
from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
