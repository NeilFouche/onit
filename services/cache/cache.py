"""
On It Cache Service

Handles cache operations
"""

import json
from django.core.cache import caches


class CacheService:
    """Handles cache operations"""

    object_cache = caches['object_cache']
    default_cache = caches['default']

    ###########################################################################
    #                          DEFAULT CACHE METHODS                          #
    ###########################################################################

    # Informational
    @staticmethod
    def get_cached_parameters():
        """Method to get the cached parameters"""

        return CacheService.default_cache.keys("*")

    @staticmethod
    def get_cache_items():
        """Method to get the cached items"""
        keys = CacheService.default_cache.keys("*")
        values = CacheService.default_cache.mget(keys)
        cache_items = dict(zip(
            [key.decode() for key in keys],
            [values.decode() for values in values]
        ))

        return cache_items

    @staticmethod
    def cache_used_memory():
        """Method to get the used memory"""
        memory_info = CacheService.default_cache.info("memory")
        return memory_info.get("used_memory_human")

    # Data management
    @staticmethod
    def add_item(context, parameter, value, expiry_time=84600):
        """
        Adds an item to the cache.

        Args:
            context (str): The context of the cache, e.g. Parameter.
            parameter_key (str): The key of the cache, Dependencies:Enquiry:Global.
            parameter_value (str): The value of the cache.
            expiry_time (int): The expiry time of the cache. Default is two days (84600 seconds).
        """
        namespaced_key = f"{context}:{parameter}"
        CacheService.default_cache.set(
            namespaced_key, json.dumps(value), timeout=expiry_time
        )

    @staticmethod
    def get_item(key=None, context=None, parameter=None):
        """
        Gets an item from the cache.

        Args:
            context (str): The context of the cache.
            parameter_key (str): The key of the cache.

        Returns:
            str: The value of the cache.
        """
        namespaced_key = key
        if not namespaced_key:
            namespaced_key = f"{context}:{parameter}"

        cached_data = CacheService.default_cache.get(namespaced_key)

        if cached_data:
            return json.loads(cached_data)

        return None

    @staticmethod
    def remove_item(context, parameter):
        """
        Removes an item from the cache.

        Args:
            context (str): The context of the cache.
            parameter_key (str): The key of the cache.
        """
        namespaced_key = f"{context}:{parameter}"
        CacheService.default_cache.delete(namespaced_key)

    @staticmethod
    def set_item(context, parameter, value, timeout=84600):
        """Method to update the cache"""
        namespaced_key = f"{context}:{parameter}"
        CacheService.default_cache.get_or_set(
            namespaced_key, json.dumps(value), timeout
        )

    @staticmethod
    def clear_cache():
        """Method to clear the cache"""

        CacheService.default_cache.clear()

    ###########################################################################
    #                          OBJECT CACHE METHODS                           #
    ###########################################################################

    # Data management
    @staticmethod
    def get_object(key):
        """
        Gets an object from the cache.

        Args:
            key (str): A hashed representation of the request.

        Returns:
            object: The cached object.
        """
        return CacheService.object_cache.get(key)

    @staticmethod
    def set_object(key, item):
        """
        Sets an object in the cache.

        Args:
            key (str): A hashed representation of the request.
            value (object): The object to cache.
        """
        CacheService.object_cache.update(key, item)

    @staticmethod
    def clear_object_cache():
        """Method to clear the object cache"""

        CacheService.object_cache.clear()
