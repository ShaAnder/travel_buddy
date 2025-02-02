from django.urls import path
from .views import home, about
# url patterns for core features
urlpatterns = [
    path("", home, name="home"),
    path("home/", home, name="home"),
    path("about/", about, name="about"),
]