"""
Message auto-delete utility
"""
import asyncio
import logging
from typing import Optional, Dict, Tuple, Union, Callable, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AutoDeleteManager:
    """
    Manages automatic deletion of messages after a specified delay.
    
    Usage:
        auto_delete = AutoDeleteManager()
        
        # Schedule deletion
        await auto_delete.schedule(
            chat_id=123,
            message_id=456,
            delay=60  # Delete after 60 seconds
        )
        
        # Delete with bot context
        await auto_delete.schedule_with_bot(
            bot=bot,
            chat_id=123,
            message_id=456,
            delay=30
        )
        
        # Cancel scheduled deletion
        auto_delete.cancel(chat_id=123, message_id=456)
        
        # Clear all scheduled deletions
        auto_delete.clear_all()
    """
    
    def __init__(self):
        self._scheduled: Dict[Tuple[int, int], asyncio.Task] = {}
        self._bot = None
    
    def set_bot(self, bot):
        """Set bot instance for automatic deletion."""
        self._bot = bot
    
    async def schedule(
        self,
        chat_id: Union[int, str],
        message_id: int,
        delay: float,
        bot = None,
        on_delete: Optional[Callable] = None
    ):
        """
        Schedule a message for deletion.
        
        Args:
            chat_id: Chat ID
            message_id: Message ID
            delay: Delay in seconds
            bot: Bot instance (if not set globally)
            on_delete: Callback after deletion
        """
        key = (chat_id, message_id)
        
        # Cancel existing task for this message
        if key in self._scheduled:
            self._cancel(key)
        
        task = asyncio.create_task(
            self._delete_after_delay(
                chat_id=chat_id,
                message_id=message_id,
                delay=delay,
                bot=bot or self._bot,
                on_delete=on_delete
            ),
            name=f"autodelete_{chat_id}_{message_id}"
        )
        
        self._scheduled[key] = task
        logger.debug(f"Scheduled deletion of message {message_id} in chat {chat_id} after {delay}s")
    
    async def schedule_with_bot(
        self,
        bot,
        chat_id: Union[int, str],
        message_id: int,
        delay: float,
        on_delete: Optional[Callable] = None
    ):
        """
        Schedule deletion with bot instance.
        
        Args:
            bot: Bot instance
            chat_id: Chat ID
            message_id: Message ID
            delay: Delay in seconds
            on_delete: Callback after deletion
        """
        await self.schedule(chat_id, message_id, delay, bot=bot, on_delete=on_delete)
    
    async def _delete_after_delay(
        self,
        chat_id: Union[int, str],
        message_id: int,
        delay: float,
        bot = None,
        on_delete: Optional[Callable] = None
    ):
        """Delete message after delay."""
        try:
            await asyncio.sleep(delay)
            
            if bot:
                await bot.delete_message(
                    chat_id=chat_id,
                    message_id=message_id
                )
                logger.debug(f"Deleted message {message_id} in chat {chat_id}")
                
                if on_delete:
                    await on_delete(chat_id, message_id, True)
            else:
                logger.warning(f"No bot available to delete message {message_id}")
                
        except asyncio.CancelledError:
            logger.debug(f"Cancelled deletion of message {message_id}")
        except Exception as e:
            logger.error(f"Failed to delete message {message_id}: {e}")
            if on_delete:
                await on_delete(chat_id, message_id, False)
        finally:
            key = (chat_id, message_id)
            if key in self._scheduled:
                del self._scheduled[key]
    
    def _cancel(self, key: Tuple):
        """Cancel a scheduled deletion."""
        if key in self._scheduled:
            task = self._scheduled[key]
            if not task.done():
                task.cancel()
            del self._scheduled[key]
    
    def cancel(self, chat_id: Union[int, str], message_id: int):
        """Cancel scheduled deletion for a message."""
        key = (chat_id, message_id)
        self._cancel(key)
    
    def cancel_chat_messages(self, chat_id: Union[int, str]):
        """Cancel all scheduled deletions for a chat."""
        keys_to_cancel = [key for key in self._scheduled if key[0] == chat_id]
        for key in keys_to_cancel:
            self._cancel(key)
        logger.debug(f"Cancelled {len(keys_to_cancel)} scheduled deletions for chat {chat_id}")
    
    def clear_all(self):
        """Cancel all scheduled deletions."""
        count = len(self._scheduled)
        for key in list(self._scheduled.keys()):
            self._cancel(key)
        logger.info(f"Cleared all {count} scheduled deletions")
    
    @property
    def pending_count(self) -> int:
        """Number of pending deletions."""
        return len(self._scheduled)
    
    @property
    def pending_messages(self) -> List[Tuple[int, int]]:
        """List of pending (chat_id, message_id) tuples."""
        return list(self._scheduled.keys())
