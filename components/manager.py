"""
Manager class for the components and services
"""

from abc import ABC, abstractmethod


class Manager(ABC):
    """Manager class for the components and services"""

    managers = {}

    @classmethod
    def register_manager(cls, name):
        """Method to register a manager"""
        def decorator(manager):
            """Decorator to register a manager"""
            cls.managers[name] = manager
            return manager
        return decorator

    @classmethod
    def get_manager(cls, name):
        """Method to get a manager"""
        return cls.managers.get(name)

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Method to execute an action"""
