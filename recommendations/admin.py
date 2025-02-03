"""
Register models for the recommendations app with the Django admin site.

This module registers the `Recommendation`, `Category`, `Comment`, and
`Vote` models, enabling them to be managed through the Django admin interface.
"""
from django.contrib import admin
from .models import Recommendation, Comment, Vote, Category

# Register your models here.
admin.site.register(Recommendation)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Vote)
