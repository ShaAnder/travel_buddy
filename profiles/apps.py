from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class ProfilesConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        logger.info("Profiles app is ready!")
        import profiles.signals