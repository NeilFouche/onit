"""
A library to handle dynamic discovery and loading of modules.
"""

import pkgutil
import importlib


def load_registered_implementations(package_name: str) -> None:
    """
    Method to import implementations of a class

    Args:
        package: The folder (package) that contains the implementations.
    """

    package = importlib.import_module(package_name)

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{package.__name__}.{module_name}")