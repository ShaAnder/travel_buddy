"""
Configure the Core application.

This module contains the configuration class for the Core app in a
Django project. It defines essential settings required for the app's
functionality.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configure the Core application settings."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
