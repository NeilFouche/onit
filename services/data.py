import json

from django.core.cache import cache
from components.sources import Source
from libs.discovery import load_registered_implementations
from services import Service
from services.rest import RestService

class DataService(Service):
    """
    Service for managing data acquisition and processing.
    """

    ###########################################################################
    #                            SOURCE MANAGEMENT                            #
    ###########################################################################

    commands = {}
    graphs = {}
    sources = {}

    @staticmethod
    def source_manager(command) -> Source:
        if not DataService.commands:
            commands_path = "data/api_specifications/commands.json"
            with open(commands_path, 'r') as file:
                DataService.commands = json.load(file)

        if command not in DataService.commands:
            raise ValueError(f"Request to '{command}' unknown. The following commands are supported: {list(DataService.commands.keys())}")

        source_label = DataService.commands[command]
        return DataService.get_source(source_label)

    @staticmethod
    def get_source(implementation: str) -> Source:
        if implementation not in DataService.sources:
            load_registered_implementations(package_name="components.sources")

        default_source = DataService.sources["Database:Default"]

        if implementation not in DataService.sources:
            source_type = implementation.split(':')[0]
            default_source = DataService.sources.get(f"{source_type}:Default", default_source)

        return DataService.sources.get(implementation, default_source)

    @staticmethod
    def register_source(label):
        def decorator(cls):
            DataService.sources[label] = cls()
            return cls
        return decorator

    ###########################################################################
    #                             DATA OPERATIONS                             #
    ###########################################################################

    @staticmethod
    def fetch_data(request_key: str):
        data = cache.get(request_key)
        if data:
            return data

        # Get data source
        command = RestService.get_command(request_key)
        data_source = DataService.source_manager(command)

        # Retrieve the data
        data = data_source.fetch(request_key)

        # Cache and return
        cache.set(request_key, data)

        return data