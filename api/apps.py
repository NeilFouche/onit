"""
This file is used to configure the app and load the configuration.
"""

import atexit
from django.apps import AppConfig
from services.configuration import ConfigurationService
from services.database.database import DatabaseService
from services.scheduling import Scheduler, ObjectCacheCleanupTask


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

        # Instantiate Singleton instances
        ApiConfig.database = DatabaseService(database="MySQL")

        # Load configuration
        ConfigurationService.load_configuration()

        # Launch scheduler
        scheduler = Scheduler()
        scheduler.add_task(ObjectCacheCleanupTask({
            "interval": 3600
        }))
        scheduler.start()

        atexit.register(scheduler.stop)
