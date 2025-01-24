"""
On It Scheduling Service - Task

A task to be scheduled
"""

from abc import ABC, abstractmethod


class Task(ABC):
    """Abstract class for a task (Inteface)"""

    def __init__(self, details):
        self.interval = details.get("interval", 0)
        self.last_run = details.get("last_run", 0)

    @abstractmethod
    def execute(self):
        """Method to execute the task"""


###############################################################################
#                            TASK IMPLEMENTATIONS                             #
###############################################################################


class ObjectCacheCleanupTask(Task):
    """
    Task to clean up the cache

    Performs basic cache cleanup:
        - Removes expired items
        - Removes oldest items if storage threshold is exceeded
    """

    def execute(self):
        """
        Runs the clean-up activities for the cache
        """
        # Remove expired items
        cache = cache.object_cache
        cache.remove_expired_items()

        # Remove oldest items if storage threshold is exceeded
        if cache.storage > cache.storage_threshold:
            cache.remove_oldest_items()
