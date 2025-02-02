"""
Core views for the application.

This module contains the views for rendering the homepage, about page,
policy page, and custom error pages. It also includes handlers for
403, 404, and 500 errors.
"""

from django.shortcuts import render

# CORE VIEWS #


def home(request):
    """
    Render the homepage of the application.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered homepage template with the navbar hidden.
    """
    image_paths = [f'images/splash_screen/splash-{i}.jpg' for i in range(1, 8)]
    return render(
        request,
        "core/home.html", {'show_navbar': False, 'image_paths': image_paths}
        )


def about(request):
    """
    Render the About page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered About page template with the navbar shown.
    """
    return render(request, "core/about.html", {'show_navbar': True})


# ERROR VIEWS #


def custom_403_view(request, exception):
    """
    Return 403 forbidden error page.

    Renders the 403 error page from 'core/templates/error/403.html'.
    """
    return render(request, 'error/403.html', status=403)
