import asyncio
from typing import Callable, List, Any
import logging

logger = logging.getLogger(__name__)


class Scheduler:
    """
    Simple scheduler for periodic task execution

    Example:
        scheduler = Scheduler()

        async def my_task():
            print("Task executed")

        scheduler.every(60, my_task)  # Every 60 seconds
        await scheduler.start()
    """

    def __init__(self):
        self.tasks: List[Callable] = []
        self._running = False

    def every(self, seconds: int, func: Callable, *args, **kwargs):
        """
        Adds a periodically executed task

        Args:
            seconds: Interval in seconds
            func: Function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
        """

        async def wrapper():
            while self._running:
                try:
                    if asyncio.iscoroutinefunction(func):
                        await func(*args, **kwargs)
                    else:
                        func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in scheduled task: {e}")
                await asyncio.sleep(seconds)

        self.tasks.append(wrapper)
        return self

    def cron(self, cron_expr: str, func: Callable, *args, **kwargs):
        """
        Adds a task executed based on a cron expression

        Requires 'croniter' library

        Args:
            cron_expr: Cron expression (e.g. "0 * * * *" - every hour)
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        try:
            from croniter import croniter
            from datetime import datetime
        except ImportError:
            raise ImportError("Please install croniter: pip install croniter")

        async def wrapper():
            base = datetime.now()
            it = croniter(cron_expr, base)

            while self._running:
                next_time = it.get_next(datetime)
                wait_seconds = (next_time - datetime.now()).total_seconds()

                if wait_seconds > 0:
                    await asyncio.sleep(wait_seconds)

                try:
                    if asyncio.iscoroutinefunction(func):
                        await func(*args, **kwargs)
                    else:
                        func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in scheduled task: {e}")

        self.tasks.append(wrapper)
        return self

    async def start(self):
        """Starts all tasks"""
        self._running = True
        await asyncio.gather(*(task() for task in self.tasks))

    def stop(self):
        """Stops all tasks"""
        self._running = False

    def clear(self):
        """Clears all tasks"""
        self.tasks.clear()
