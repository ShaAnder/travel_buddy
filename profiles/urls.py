from django.urls import path
from .views import profile_view

#creating a path to our profile and a path to edit the profile
urlpatterns = [
    path("profile/", profile_view, name="profile"),
    # path("edit/", edit_profile_view, name="edit_profile"),
]