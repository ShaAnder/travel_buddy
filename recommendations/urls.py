from django.urls import path
from .views import recommendations, add_recommendation

urlpatterns = [
    path("recommendations/", recommendations, name="recommendations"),
    path("add_recommendation/", add_recommendation, name="add_recommendation"),
]