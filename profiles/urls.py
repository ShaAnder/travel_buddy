from django.urls import path
from .views import profile, signup_login

#creating a path to our profile and a path to edit the profile
urlpatterns = [
    path("profile/", profile, name="profile"),
    path("login/", signup_login, name="login")
]

