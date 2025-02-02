"""
Define URL patterns for user account and profile management.

This module specifies the URL configurations for managing user profiles
and account-related actions (login, signup, password reset, logout) in
the application. It includes paths for viewing, editing, and deleting
profiles, as well as handling authentication through Django Allauth.
"""
from django.urls import path, include
from allauth.account.views import LoginView, SignupView, PasswordResetView
from . import views

urlpatterns = [
    # Profile URL patterns
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/delete_profile/', views.delete_account, name='delete_account'),
    # Account URL patterns
    path('accounts/login/', LoginView.as_view(template_name="allauth/account/login.html"), name="account_login"),
    # Signup
    path('accounts/signup/', SignupView.as_view(template_name="allauth/account/signup.html"), name="account_signup"),
    # Password Reset
    path('accounts/password/reset/', PasswordResetView.as_view(template_name="allauth/account/password_reset.html"), name="account_reset_password"),
    # logout
    path("logout/", views.logout, name="logout"),
    # Include allauth URLs
    path('accounts/', include('allauth.urls')),  
]
