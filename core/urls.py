from django.urls import path
from .views import home

# url patterns for core features
urlpatterns = [
    path("", home, name="home"),
]