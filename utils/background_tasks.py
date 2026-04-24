"""
Background tasks API for Dispatcher
"""
import asyncio
import logging
from typing import Callable, Any, Dict, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class BackgroundTask:
    """Represents a background task."""
    name: str
    coro: Callable
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    task: Optional[asyncio.Task] = None
    on_start: Optional[Callable] = None
    on_stop: Optional[Callable] = None
    restart_on_failure: bool = False
    max_retries: int = 3
    retry_delay: float = 5.0


class BackgroundTasksManager:
    """
    Manages background tasks for the dispatcher.
    
    Usage:
        # In dispatcher or bot setup:
        bg = BackgroundTasksManager()
        
        # Add task
        bg.add_task("monitor", monitor_function)
        
        # Start all tasks
        await bg.start_all()
        
        # Stop all tasks
        await bg.stop_all()
    """
    
    def __init__(self):
        self._tasks: Dict[str, BackgroundTask] = {}
        self._running = False
    
    def add_task(
        self,
        name: str,
        coro: Callable,
        *args,
        on_start: Optional[Callable] = None,
        on_stop: Optional[Callable] = None,
        restart_on_failure: bool = False,
        max_retries: int = 3,
        retry_delay: float = 5.0,
        **kwargs
    ):
        """
        Add a background task.
        
        Args:
            name: Task name
            coro: Async function to run
            *args: Arguments to pass
            on_start: Callback on start
            on_stop: Callback on stop
            restart_on_failure: Restart if task fails
            max_retries: Max restart attempts
            retry_delay: Delay between retries
            **kwargs: Keyword arguments
        """
        self._tasks[name] = BackgroundTask(
            name=name,
            coro=coro,
            args=args,
            kwargs=kwargs,
            on_start=on_start,
            on_stop=on_stop,
            restart_on_failure=restart_on_failure,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
        logger.debug(f"Added background task: {name}")
    
    async def start_task(self, name: str):
        """Start a specific task."""
        if name not in self._tasks:
            raise KeyError(f"Task not found: {name}")
        
        task_info = self._tasks[name]
        
        if task_info.task and not task_info.task.done():
            logger.warning(f"Task {name} is already running")
            return
        
        if task_info.on_start:
            try:
                await task_info.on_start()
            except Exception as e:
                logger.error(f"Error in on_start for {name}: {e}")
        
        task_info.task = asyncio.create_task(
            self._run_task(task_info),
            name=name
        )
        logger.info(f"Started background task: {name}")
    
    async def _run_task(self, task_info: BackgroundTask):
        """Run a task with retry logic."""
        retries = 0
        
        while True:
            try:
                await task_info.coro(*task_info.args, **task_info.kwargs)
                break  # Task completed successfully
            except asyncio.CancelledError:
                logger.info(f"Task {task_info.name} was cancelled")
                break
            except Exception as e:
                retries += 1
                logger.error(
                    f"Error in task {task_info.name} "
                    f"(attempt {retries}/{task_info.max_retries}): {e}"
                )
                
                if task_info.restart_on_failure and retries < task_info.max_retries:
                    logger.info(f"Restarting task {task_info.name} in {task_info.retry_delay}s...")
                    await asyncio.sleep(task_info.retry_delay)
                else:
                    logger.error(f"Task {task_info.name} failed permanently")
                    break
    
    async def stop_task(self, name: str):
        """Stop a specific task."""
        if name not in self._tasks:
            raise KeyError(f"Task not found: {name}")
        
        task_info = self._tasks[name]
        
        if task_info.task and not task_info.task.done():
            task_info.task.cancel()
            try:
                await task_info.task
            except asyncio.CancelledError:
                pass
            
            if task_info.on_stop:
                try:
                    await task_info.on_stop()
                except Exception as e:
                    logger.error(f"Error in on_stop for {name}: {e}")
            
            logger.info(f"Stopped background task: {name}")
    
    async def start_all(self):
        """Start all registered tasks."""
        self._running = True
        for name in self._tasks:
            await self.start_task(name)
    
    async def stop_all(self):
        """Stop all running tasks."""
        self._running = False
        for name in list(self._tasks.keys()):
            await self.stop_task(name)
    
    def is_running(self, name: str) -> bool:
        """Check if a task is running."""
        if name not in self._tasks:
            return False
        return self._tasks[name].task is not None and not self._tasks[name].task.done()
    
    @property
    def running_tasks(self) -> List[str]:
        """Get list of running task names."""
        return [name for name in self._tasks if self.is_running(name)]
    
    @property
    def all_tasks(self) -> Dict[str, BackgroundTask]:
        """Get all tasks."""
        return self._tasks.copy()
