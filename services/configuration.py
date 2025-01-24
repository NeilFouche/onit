"""
On It Configuration Service

Handles configuration operations

Operations:
    - get_parameter
    - add_parameter
    - update_parameter
"""

import json
from django.core.cache import cache
from services.database import DatabaseService


class ConfigurationService:
    """
    Handles configuration operations
    """

    _parameters = {}

    @staticmethod
    def cache_configuration():
        """
        Method to cache the configuration
        """
        onitdb = DatabaseService.get_database()
        parameters = onitdb.parameter.all()

        if not parameters:
            return None

        for parameter in parameters:
            key = parameter["key"]
            value = parameter["value"]

            ConfigurationService._parameters[key] = value

            if key and value:
                cache.set(key, json.dumps(value))

    @staticmethod
    def load_configuration():
        """
        Method to load the configuration
        """
        ConfigurationService._parameters = ConfigurationService.get_parameter(
            category="Configuration", key="AppConfig"
        ) or {}

        if not ConfigurationService._parameters:
            ConfigurationService.cache_configuration()

    @staticmethod
    def get_parameter(category, key, scope="Global"):
        """
        Method to get a parameter by key
        """
        namespaced_key = f"{category}:{key}:{scope}"
        return ConfigurationService._parameters.get(namespaced_key, None)

    @staticmethod
    def add_parameter(parameter_data):
        """
        Method to add a parameter
        """
        onitdb = DatabaseService.get_database()
        onitdb.parameter.add(parameter_data.to_dict)

        return cache.add_item(
            context="Parameter", parameter=parameter_data.key, value=parameter_data.value
        )

    @staticmethod
    def update_parameter(category, key, value, scope="Global"):
        """
        Method to update a parameter
        """
        onitdb = DatabaseService.get_database()
        namespaced_key = f"{category}:{key}:{scope}"
        instance = onitdb.parameter.get(key=namespaced_key)

        if instance:
            if "value" not in instance:
                return None

            current_value = instance.get("value", None)
            if current_value != value:
                instance["value"] = value
                onitdb.parameter.update(instance)

            return cache.set_item(
                context="Parameter", parameter=namespaced_key, value=value
            )

        return None
