from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """ProfileConfig Class

    Args:
        AppConfig (Class): the default app config from django apps
    
    Description:
        Config file for the profile signal, the profiles.signal
        is greyed out here as it's not used, but will be used as
        soon as the signal is fired
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        import profiles.signals