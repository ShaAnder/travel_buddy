"""
Configure the Recommendations application.

This module defines the configuration class for
the Recommendations app, specifying essential settings
required for its functionality within the Django project.
"""
from django.apps import AppConfig


class RecommendationsConfig(AppConfig):
    """
    Configure the Recommendations app.

    This class sets up the configuration for the Recommendations app,
    including defining the default auto field type for model
    IDs and the app's name.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recommendations'
