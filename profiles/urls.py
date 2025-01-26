from django.urls import path, include
from .views import profile

from allauth.account.views import login, signup

# creating a path to our profile and a path to edit the profile
urlpatterns = [
    path("profile/", profile, name="profile"),
]



urlpatterns = [
    # I wanted to have cleaner custom urls, so we can override
    # the defaults for login / signup and keep the rest as normal
    path('account/login/', login, name='account_login'), 
    path('account/signup/', signup, name='account_signup'),
    path('accounts/', include('allauth.urls')),
]