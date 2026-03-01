import asyncio
from typing import Callable, List, Any
import logging

logger = logging.getLogger(__name__)


class Scheduler:
    """
    Prosty scheduler do okresowego wykonywania zadań

    Przykład:
        scheduler = Scheduler()

        async def my_task():
            print("Task executed")

        scheduler.every(60, my_task)  # Co 60 sekund
        await scheduler.start()
    """

    def __init__(self):
        self.tasks: List[Callable] = []
        self._running = False

    def every(self, seconds: int, func: Callable, *args, **kwargs):
        """
        Dodaje zadanie wykonywane okresowo

        Args:
            seconds: Interwał w sekundach
            func: Funkcja do wykonania
            *args: Argumenty pozycyjne dla funkcji
            **kwargs: Argumenty nazwane dla funkcji
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
        Dodaje zadanie wykonywane według wyrażenia cron

        Wymaga biblioteki 'croniter'

        Args:
            cron_expr: Wyrażenie cron (np. "0 * * * *" - co godzinę)
            func: Funkcja do wykonania
            *args: Argumenty pozycyjne
            **kwargs: Argumenty nazwane
        """
        try:
            from croniter import croniter
            from datetime import datetime
        except ImportError:
            raise ImportError("Please install croniter: pip install croniter")

        async def wrapper():
            base = datetime.now()
            iter = croniter(cron_expr, base)

            while self._running:
                next_time = iter.get_next(datetime)
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
        """Uruchamia wszystkie zadania"""
        self._running = True
        await asyncio.gather(*(task() for task in self.tasks))

    def stop(self):
        """Zatrzymuje wszystkie zadania"""
        self._running = False

    def clear(self):
        """Czyści wszystkie zadania"""
        self.tasks.clear()