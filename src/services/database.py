"""
On It Database Service - Database

Handles database operations

Databases:
    - MySQLDatabase
"""

from libs.discovery import load_registered_implementations
from components.protocols import RelationalDatabase


class DatabaseService():

    databases = {}

    @staticmethod
    def get_database(implementation: str = "PostgreSQL") -> RelationalDatabase:
        """
        Method to get the database
        """
        if implementation not in DatabaseService.databases:
            load_registered_implementations(package_name="components.sources.databases")

        default_database = DatabaseService.databases['PostgreSQL']
        database = DatabaseService.databases.get(implementation, default_database)

        return database

    @staticmethod
    def register_database(implementation: str):
        def decorator(cls):
            DatabaseService.databases[implementation] = cls()
            return cls
        return decorator
