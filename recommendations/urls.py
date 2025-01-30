from django.urls import path
from .views import recommendations, add_recommendation, edit_recommendation, delete_recommendation

urlpatterns = [
    path("recommendations/", recommendations, name="recommendations"),
    path('add-recommendation/', add_recommendation, name='add_recommendation'),
    path("edit_recommendation/<int:recommendation_id>/", edit_recommendation, name="edit_recommendation"),
    path("delete_recommendation/<int:recommendation_id>/", delete_recommendation, name="delete_recommendation"),
]