"""
Admin broadcast utility - Send messages to all chats with rate limiting
"""
import asyncio
import logging
from typing import List, Union, Optional, Dict, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class BroadcastResult:
    """Result of a broadcast operation."""
    success_count: int = 0
    failure_count: int = 0
    blocked_count: int = 0
    errors: List[Dict[str, Any]] = field(default_factory=list)
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    
    @property
    def total(self) -> int:
        return self.success_count + self.failure_count + self.blocked_count
    
    @property
    def success_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return (self.success_count / self.total) * 100


class BroadcastManager:
    """
    Manages broadcasting messages to multiple chats with rate limiting.
    
    Usage:
        broadcast = BroadcastManager(bot)
        
        # Broadcast to all known chats
        result = await broadcast.send_to_chats(
            chat_ids=[123, 456, 789],
            text="Important announcement!",
            rate_limit=0.05  # 50ms between messages
        )
        
        print(f"Success: {result.success_count}, Failed: {result.failure_count}")
    """
    
    def __init__(self, bot, chat_ids: Optional[List[Union[int, str]]] = None):
        """
        Args:
            bot: Bot instance
            chat_ids: List of chat IDs to broadcast to
        """
        self.bot = bot
        self._chat_ids: List[Union[int, str]] = chat_ids or []
        self._is_running = False
    
    def add_chat(self, chat_id: Union[int, str]):
        """Add a chat to the broadcast list."""
        if chat_id not in self._chat_ids:
            self._chat_ids.append(chat_id)
    
    def remove_chat(self, chat_id: Union[int, str]):
        """Remove a chat from the broadcast list."""
        if chat_id in self._chat_ids:
            self._chat_ids.remove(chat_id)
    
    def clear_chats(self):
        """Clear all chats from the broadcast list."""
        self._chat_ids.clear()
    
    @property
    def chat_ids(self) -> List[Union[int, str]]:
        """Get all chat IDs."""
        return self._chat_ids.copy()
    
    async def send_to_chats(
        self,
        chat_ids: Optional[List[Union[int, str]]] = None,
        text: str = "",
        parse_mode: Optional[str] = None,
        disable_web_page_preview: bool = False,
        reply_markup: Optional[Dict] = None,
        rate_limit: float = 0.05,
        on_progress: Optional[Callable] = None,
        on_error: Optional[Callable] = None,
        include_photo: Optional[str] = None,
        **kwargs
    ) -> BroadcastResult:
        """
        Broadcast a message to multiple chats.
        
        Args:
            chat_ids: Chats to send to (uses internal list if None)
            text: Message text
            parse_mode: Parse mode (Markdown, HTML)
            disable_web_page_preview: Disable link previews
            reply_markup: Reply markup
            rate_limit: Seconds between messages (default 50ms)
            on_progress: Callback(current, total, chat_id, success)
            on_error: Callback(chat_id, error)
            include_photo: Optional photo URL/file_id
            **kwargs: Additional send_message arguments
            
        Returns:
            BroadcastResult with statistics
        """
        target_chats = chat_ids or self._chat_ids
        
        if not target_chats:
            logger.warning("No chats to broadcast to")
            return BroadcastResult()
        
        self._is_running = True
        result = BroadcastResult(
            started_at=datetime.now()
        )
        
        total = len(target_chats)
        logger.info(f"Starting broadcast to {total} chats")
        
        for i, chat_id in enumerate(target_chats, 1):
            if not self._is_running:
                logger.info("Broadcast cancelled")
                break
            
            try:
                if include_photo:
                    await self.bot.send_photo(
                        chat_id=chat_id,
                        photo=include_photo,
                        caption=text,
                        parse_mode=parse_mode,
                        reply_markup=reply_markup,
                        **kwargs
                    )
                else:
                    await self.bot.send_message(
                        chat_id=chat_id,
                        text=text,
                        parse_mode=parse_mode,
                        disable_web_page_preview=disable_web_page_preview,
                        reply_markup=reply_markup,
                        **kwargs
                    )
                
                result.success_count += 1
                logger.debug(f"Broadcast success: {chat_id}")
                
                if on_progress:
                    await on_progress(i, total, chat_id, True)
                
            except Exception as e:
                error_str = str(e).lower()
                
                # Detect blocked users
                if 'blocked' in error_str or 'forbidden' in error_str:
                    result.blocked_count += 1
                    logger.debug(f"Blocked user: {chat_id}")
                else:
                    result.failure_count += 1
                    result.errors.append({
                        'chat_id': chat_id,
                        'error': str(e)
                    })
                    logger.warning(f"Broadcast failed for {chat_id}: {e}")
                    
                    if on_error:
                        await on_error(chat_id, e)
                
                if on_progress:
                    await on_progress(i, total, chat_id, False)
            
            # Rate limiting
            if i < total:
                await asyncio.sleep(rate_limit)
        
        result.finished_at = datetime.now()
        self._is_running = False
        
        logger.info(
            f"Broadcast completed: "
            f"{result.success_count} success, "
            f"{result.blocked_count} blocked, "
            f"{result.failure_count} failed"
        )
        
        return result
    
    def stop(self):
        """Stop the current broadcast."""
        self._is_running = False
    
    @property
    def is_running(self) -> bool:
        """Check if a broadcast is currently running."""
        return self._is_running
