from django.apps import AppConfig
import logging

# Initialize logger for this module
logger = logging.getLogger(__name__)

class ProfilesConfig(AppConfig):
    """
    Configuration class for the Profiles app.

    Args:
        name (str): The name of the app, which is 'profiles'.
    
    Description:
        This class initializes the Profiles app and logs when it is ready.
        It also imports the signals to link them with the app once the app is ready.
    """
    name = 'profiles'

    def ready(self):
        """
        Runs when the Profiles app is fully loaded and ready.

        Logs an informational message and imports the signals module to connect signals
        with the app.
        """
        # Log that the Profiles app is ready
        logger.info("Profiles app is ready!")

        # Import signals to ensure they're linked when the app is ready
        import profiles.signals
