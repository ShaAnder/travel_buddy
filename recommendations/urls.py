"""
URLs for the Recommendations app.

This module defines the URL patterns for the `Recommendations` app, including 
both regular views and API views. The regular views include pages for listing, 
adding, editing, and deleting recommendations. The API views are handled using 
Django REST framework's `DefaultRouter`, which automatically creates routes 
for the `RecommendationViewSet` and `CategoryViewSet`.
"""
from django.urls import path, include
from recommendations.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'recommendations', RecommendationViewSet)
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path("recommendations/", recommendations, name="recommendations"),
    path('add-recommendation/', add_recommendation, name='add_recommendation'),
    path("edit_recommendation/<int:recommendation_id>/", edit_recommendation, name="edit_recommendation"),
    path("delete_recommendation/<int:recommendation_id>/", delete_recommendation, name="delete_recommendation"),
    path('api/', include(router.urls)),
]