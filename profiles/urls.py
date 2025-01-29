from django.urls import path, include
from . import views

urlpatterns = [
    # Profile URL patterns
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/delete_profile/', views.delete_account, name='delete_account'),
    # Account URL patterns
    path('account/login/', views.login, name='account_login'),
    path('account/signup/', views.signup, name='account_signup'),
    path('accounts/', include('allauth.urls')),
    path('account/logout/', views.logout, name='account_logout')
]