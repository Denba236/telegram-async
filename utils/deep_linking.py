"""
Deep linking helpers for Telegram bots
"""
from typing import Optional, Union
import base64
import logging

logger = logging.getLogger(__name__)


class DeepLink:
    """
    Helper for creating Telegram deep links.
    
    Usage:
        link = DeepLink.create_start_link(bot_username, param="ref_123")
        # Returns: https://t.me/YourBot?start=ref_123
        
        # With group:
        link = DeepLink.create_start_group_link(bot_username, group_username)
        # Returns: https://t.me/YourBot?startgroup=group_username
    """
    
    @staticmethod
    def create_start_link(
        bot_username: str,
        param: Optional[str] = None,
        encode: bool = False
    ) -> str:
        """
        Create a /start deep link.
        
        Args:
            bot_username: Bot username (without @)
            param: Parameter to pass to /start
            encode: Base64 encode the parameter
            
        Returns:
            Full URL
        """
        base_url = f"https://t.me/{bot_username}"
        
        if param:
            if encode:
                # Base64 encode to handle special characters
                param = base64.urlsafe_b64encode(param.encode('utf-8')).decode('utf-8').rstrip('=')
            
            return f"{base_url}?start={param}"
        
        return base_url
    
    @staticmethod
    def create_start_group_link(
        bot_username: str,
        group_username: str
    ) -> str:
        """
        Create a /start group link (adds bot to group).
        
        Args:
            bot_username: Bot username (without @)
            group_username: Group username (without @)
            
        Returns:
            Full URL
        """
        return f"https://t.me/{bot_username}?startgroup={group_username}"
    
    @staticmethod
    def create_share_link(
        url: str,
        text: Optional[str] = None
    ) -> str:
        """
        Create a share link.
        
        Args:
            url: URL to share
            text: Optional text
            
        Returns:
            Full URL
        """
        from urllib.parse import quote
        
        params = f"url={quote(url, safe='')}"
        if text:
            params += f"&text={quote(text, safe='')}"
        
        return f"https://t.me/share/url?{params}"
    
    @staticmethod
    def create_join_link(group_username: str) -> str:
        """
        Create a join group link.
        
        Args:
            group_username: Group username (without @)
            
        Returns:
            Full URL
        """
        return f"https://t.me/+{group_username}"
    
    @staticmethod
    def create_telegram_link(url: str) -> str:
        """
        Create a t.me link.
        
        Args:
            url: Path after t.me/
            
        Returns:
            Full URL
        """
        return f"https://t.me/{url}"
    
    @staticmethod
    def parse_start_param(param: str, decode: bool = False) -> str:
        """
        Parse /start parameter.
        
        Args:
            param: Start parameter
            decode: Base64 decode the parameter
            
        Returns:
            Decoded parameter
        """
        if decode:
            try:
                # Add padding if needed
                padding = 4 - len(param) % 4
                if padding != 4:
                    param += '=' * padding
                return base64.urlsafe_b64decode(param).decode('utf-8')
            except Exception:
                logger.warning(f"Failed to decode start parameter: {param}")
                return param
        return param
