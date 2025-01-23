from django.urls import path
from .views import profile

#creating a path to our profile and a path to edit the profile
urlpatterns = [
    path("profile/", profile, name="profile"),
]

