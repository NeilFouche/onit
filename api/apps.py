"""
This file is used to configure the app and load the configuration.
"""

from django.apps import AppConfig

class ApiConfig(AppConfig):
    """
    ApiConfig class
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    database = None

    def ready(self):
        """
        Method to configure the app
        """
        from django.contrib.sessions.models import Session

        # Update constants in memory now that the App is ready
        from onit.constants import EMPTY_QUERYSET
        EMPTY_QUERYSET = Session.objects.none()

        from services.configuration import ConfigurationService
        from services.database import DatabaseService
        from services.rest import RestService

        # Load configuration
        ConfigurationService.load_configuration()

        # Instantiate Singleton instances
        ApiConfig.database = DatabaseService.get_database()

        # Load RestService configuration
        RestService.get_control_parameters()