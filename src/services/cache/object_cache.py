"""
On It Cache Service - ObjectCache

Handles caching for complex objects.
"""

import sys
from time import time
from django.core.cache.backends.base import BaseCache
from services.configuration import ConfigurationService


class ObjectCache(BaseCache):
    """Handles caching for complex objects"""

    def __init__(self, params=None, *args, **kwargs):
        self._cached_objects = {}
        self._object_metadata = {}
        self.storage = 0
        self._timeout = 0
        self.storage_threshold = 0

        params = params or {}
        super().__init__(params)

    def add(self, key, value, timeout=None, version=None):
        """
        Adds an object to the cache.

        Args:
            key (str): A hashed representation of the request.
            item (object): The object to be cached.
        """
        if key in self._cached_objects:
            return False

        self.set(key, value, timeout, version)
        return True

    def set(self, key, value, timeout=None, version=None):
        """
        Sets an object on the cache.

        Args:
            key (str): A hashed representation of the request.
            item (object): The object to be cached.
        """
        # Provision storage for the new item
        item_size = sys.getsizeof(value)

        if not self.storage_threshold:
            self._refresh_configuration()

        if self.storage + item_size > self.storage_threshold:
            self.remove_oldest_objects()

        # Add the item to the cache
        self._object_metadata[key] = {
            "created_at": time(),
            "expires_at": time() + self._timeout,
            "size": item_size,
        }
        self._cached_objects[key] = value
        self._update_storage(key, value)

    def get(self, key, default=None, version=None):
        """
        Gets an object from the cache.

        Args:
            key (str): A hashed representation of the request.

        Returns:
            object: The cached object.
        """
        if not key in self._cached_objects:
            return None

        self._reset_timeout(key)

        return self._cached_objects.get(key, None)

    def print_info(self):
        print(f"Number of cached objects: {len(self._cached_objects)}")

    def delete(self, key, version=None):
        """
        Deletes an object from the cache.

        Args:
            key (str): A hashed representation of the request.
        """
        self._cached_objects.pop(key, None)
        item = self._object_metadata.pop(key, None)
        self.storage -= item["size"]

    def clear(self):
        """Clears the cache."""
        self._cached_objects = {}
        self._object_metadata = {}
        self.storage = 0

    def _reset_timeout(self, key):
        """
        Resets the timeout for an object.

        Args:
            key (str): A hashed representation of the request.
        """
        self._object_metadata[key]["expires_at"] = time() + self._timeout

    def _update_storage(self, key, item=None):
        """
        Resets the timeout for an object.

        Args:
            key (str): A hashed representation of the request.
        """
        item_size = sys.getsizeof(item)
        self._object_metadata[key]["size"] = item_size
        self.storage += item_size

    def remove_expired_objects(self):
        """Removes objects that have expired."""
        current_time = time()

        for key, value in self._object_metadata.items():
            if current_time > value["expires_at"]:
                self.delete(key)

    def remove_oldest_objects(self):
        """Removes the oldest objects until the storage is below the threshold."""
        if not self.storage_threshold:
            self._refresh_configuration()

        while self.storage > self.storage_threshold:
            oldest_key = min(
                self._object_metadata, key=lambda k: self._object_metadata[k]["created_at"]
            )
            self.delete(oldest_key)

    def _refresh_configuration(self):
        """Refreshes the configuration."""
        self._timeout = int(ConfigurationService.get_parameter(
            category="Cache", key="ObjectCacheTimeout"
        ) or '86400')
        self.storage_threshold = int(ConfigurationService.get_parameter(
            category="Cache", key="ObjectCacheStorageThreshold"
        ) or '52428800')

    def get_many(self, keys, version=None):
        return super().get_many(keys, version)

    def set_many(self, data, timeout=None, version=None):
        return super().set_many(data, timeout, version)
