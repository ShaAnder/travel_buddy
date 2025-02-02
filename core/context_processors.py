"""
Set up the Core application.

This module defines the Core app's configuration class, specifying
essential settings required for its functionality within the Django project.
"""


def navbar_visibility(request):
    """
    Navbar Processor.

    Args:
        request()

    Description:
        custom processor for navbar visibility want to disable the navbar for
        certain pages only (like the splash screen) and not have to handle
        repeating the code to show it in every page.

    Returns:
        context for if the navbar should be shown or not
    """
    if request.path == '':
        return {'show_navbar': False}
    return {'show_navbar': True}
