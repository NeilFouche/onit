"""
On It Configuration Service

Handles configuration operations

Operations:
    - get_parameter
    - add_parameter
    - update_parameter
"""

import csv
from django.core.cache import cache
from libs.strings import format_value
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
                cache.set(key, value)

    @staticmethod
    def load_configuration():
        """
        Method to load the configuration
        """
        if not ConfigurationService._parameters:
            # import config
            config_path = "config/parameters.csv"
            with open(config_path, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                _ = next(csv_reader)

                for row in csv_reader:
                    key, value, dtype = row[1], row[5], row[7]
                    ConfigurationService._parameters[key] = format_value(value, dtype)
                    if key and ConfigurationService._parameters[key]:
                        cache.set(key, value)

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
        onitdb.parameter.create(parameter_data.to_dict)

        return cache.set(
            key=f"Parameter:{parameter_data.key}", value=parameter_data.value
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
            if not hasattr(instance, "value"):
                return None

            current_value = getattr(instance, "value")
            if current_value != value:
                setattr(instance, "value", value)
                onitdb.parameter.update(instance)

            cache.set(
                key=f"Parameter:{namespaced_key}", value=value
            )

            return value

        return None
