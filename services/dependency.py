"""
On It Dependency Service

Handles dependency operations
"""

import os
import importlib


class DependencyService():
    """Handles dependency operations"""

    @staticmethod
    def load_registered_implementations(parent, package):
        """
        Method to import implementations of a class

        Args:
            cls (str): The parent (interface) of this implementation.
            package (str): The package to import the implementations from.
        """
        package_files = [f for f in os.listdir(
            package) if f.endswith(".py") and not f.startswith("__")]

        for file in package_files:
            module_name = file[:-3]
            package_import_string = package.replace("/", ".")
            module = importlib.import_module(
                f"{package_import_string}.{module_name}"
            )

            # Register all classes that have been decorated with the @register decorator
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if hasattr(attr, "_is_registered"):
                    parent.register_implementation(attr.__name__, attr)
