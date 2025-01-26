from django.urls import path, include
from . import views


urlpatterns = [
    # creating a path to our profile
    path("profile/", views.profile, name="profile"),

    # I wanted to have cleaner custom urls, so we can override
    # the defaults for login / signup and keep the rest as normal
    path('account/login/', views.login, name='account_login'), 
    path('account/signup/', views.signup, name='account_signup'),
    path('accounts/', include('allauth.urls')),
    path('account/logout/', views.logout, name='account_logout')
]