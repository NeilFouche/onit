"""
On It Schdeuling Service - Scheduler

Handles scheduling operations
"""

from concurrent.futures import ThreadPoolExecutor
import threading
import time


class Scheduler:
    """Handles scheduling operations"""

    def __init__(self):
        self.tasks = []
        self.running = False
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=10)

    def add_task(self, task):
        """
        Registers a task to be executed at a fixed interval.

        Args:
            func (callable): The function to execute.
            interval (float): Interval in seconds between executions.
        """
        with self.lock:
            self.tasks.append(task)

    def _run(self):
        """Runs the scheduler"""
        while self.running:
            now = time.time()
            with self.lock:
                for task in self.tasks:
                    if now - task.last_run >= task.interval:
                        self.executor.submit(task.execute)
                        task.last_run = now
            time.sleep(1)  # Adjust this for granularity

    def start(self):
        """Starts the scheduler"""
        if not self.running:
            self.running = True
            threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        """Stops the scheduler"""
        self.running = False
