"""
On It Cache Service

Handles cache operations
"""

from django.core.cache import cache


class CacheService:
    """Handles cache operations"""

    @staticmethod
    def get_object(key):
        """
        Gets an object from the cache.

        Args:
            key (str): A hashed representation of the request.

        Returns:
            object: The cached object.
        """
        return cache.get(key)

    @staticmethod
    def set_object(key, item):
        """
        Sets an object in the cache.

        Args:
            key (str): A hashed representation of the request.
            value (object): The object to cache.
        """
        cache.update(key, item)

    @staticmethod
    def clear_object_cache():
        """Method to clear the object cache"""

        cache.clear()

    @staticmethod
    def print_info():
        """Method to print the cache info"""
        cache.print_info()
        print(
            f"Used memory: {cache.object_cache.storage} ({cache.object_cache.storage_threshold})")
