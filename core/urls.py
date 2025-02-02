from django.urls import path
from .views import home, about, policy

# url patterns for core features
urlpatterns = [
    path("", home, name="home"),
    path("home/", home, name="home"),
    path("policy/", policy, name="policy"),
    path("about/", about, name="about"),
]