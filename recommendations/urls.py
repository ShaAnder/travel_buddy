from django.urls import path, include
from recommendations.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'recommendations', RecommendationViewSet)

urlpatterns = [
    path("recommendations/", recommendations, name="recommendations"),
    path('add-recommendation/', add_recommendation, name='add_recommendation'),
    path("edit_recommendation/<int:recommendation_id>/", edit_recommendation, name="edit_recommendation"),
    path("delete_recommendation/<int:recommendation_id>/", delete_recommendation, name="delete_recommendation"),
    path('api/', include(router.urls)),
]