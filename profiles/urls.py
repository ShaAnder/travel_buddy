from django.urls import path, include
from . import views


urlpatterns = [
    # PROFILE URL PATTERS
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),

    # ACCOUNT URL PATTERNS
    path('account/login/', views.login, name='account_login'), 
    path('account/signup/', views.signup, name='account_signup'),
    #no actual view or template for accounts it's part of allauths url structure
    path('accounts/', include('allauth.urls')),
    path('account/logout/', views.logout, name='account_logout')
    # I wanted to have cleaner custom urls, so we can override
    # the defaults for login / signup and keep the rest as normal
]