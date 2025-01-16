"""
Data Class for Parameter Data
"""

from typing import Any
from dataclasses import dataclass


@dataclass
class ParameterData:
    """
    Data class for Parameter Data
    """
    key: str
    label: str
    slug: str
    description: str
    value: Any
    default: str
    data_type: str
    category: str
    scope: str
    namespaced_key: str

    @property
    def namespaced_key(self):
        """
        Property to get the namespaced key
        """
        return f"{self.category}:{self.key}:{self.scope}"

    @property
    def data_type(self):
        """
        Property to get the data type
        """
        return type(self.value).__name__

    def to_dict(self):
        """
        Method to convert the data class to a dictionary
        """
        return {
            "key": self.namespaced_key,
            "label": self.label,
            "slug": self.slug,
            "description": self.description,
            "value": self.value,
            "default": self.default,
            "data_type": self.data_type,
            "category": self.category,
            "scope": self.scope,
        }
