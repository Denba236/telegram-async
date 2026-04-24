"""
Callback Data Factory - Auto-encode/decode callback data
"""
import struct
import base64
import logging
from typing import Dict, Any, Optional, Type, List
from dataclasses import dataclass, fields, is_dataclass

logger = logging.getLogger(__name__)


class CallbackData:
    """
    Factory for creating structured callback data.
    
    Usage:
        class VoteCallback(CallbackData):
            prefix = "vote"
            post_id: int
            user_action: str
        
        # Create:
        callback = VoteCallback.new(post_id=123, user_action="upvote")
        # Returns: "vote:123:upvote"
        
        # Parse:
        data = VoteCallback.parse(callback)
        # Returns: {"post_id": 123, "user_action": "upvote"}
    """
    
    prefix: str = "cb"
    
    @classmethod
    def new(cls, **kwargs) -> str:
        """
        Create callback data string.
        
        Args:
            **kwargs: Field values
            
        Returns:
            Encoded callback string
        """
        if not hasattr(cls, 'prefix'):
            raise ValueError(f"CallbackData subclass must define 'prefix'")
        
        parts = [cls.prefix]
        
        # Get fields from class annotations or dataclass
        field_names = []
        if is_dataclass(cls):
            field_names = [f.name for f in fields(cls)]
        elif hasattr(cls, '__annotations__'):
            field_names = list(cls.__annotations__.keys())
        
        for field_name in field_names:
            value = kwargs.get(field_name, "")
            parts.append(str(value))
        
        # Telegram callback data limit is 64 bytes
        result = ":".join(parts)
        if len(result.encode('utf-8')) > 64:
            raise ValueError(f"Callback data too long: {len(result)} bytes (max 64)")
        
        return result
    
    @classmethod
    def parse(cls, data: str) -> Dict[str, Any]:
        """
        Parse callback data string.
        
        Args:
            data: Callback data string
            
        Returns:
            Dict of field names and values
        """
        parts = data.split(":")
        
        if parts[0] != cls.prefix:
            raise ValueError(f"Invalid prefix: {parts[0]} (expected {cls.prefix})")
        
        # Get fields
        field_names = []
        if is_dataclass(cls):
            field_names = [f.name for f in fields(cls)]
        elif hasattr(cls, '__annotations__'):
            field_names = list(cls.__annotations__.keys())
        
        if len(parts) - 1 != len(field_names):
            raise ValueError(f"Field count mismatch: got {len(parts) - 1}, expected {len(field_names)}")
        
        result = {}
        for i, field_name in enumerate(field_names):
            value = parts[i + 1]
            
            # Try to convert to original type
            if hasattr(cls, '__annotations__'):
                field_type = cls.__annotations__.get(field_name)
                if field_type == int:
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                elif field_type == bool:
                    value = value.lower() in ('true', '1', 'yes')
            
            result[field_name] = value
        
        return result
    
    @classmethod
    def validate(cls, data: str) -> bool:
        """Check if data string matches this callback's prefix."""
        return data.startswith(cls.prefix + ":")


class CompactCallbackData(CallbackData):
    """
    Compact callback data using base64 encoding for longer data.
    
    Usage:
        class PageCallback(CompactCallbackData):
            prefix = "pg"
        
        callback = PageCallback.new(page=123, sort="date")
        # Returns: "pg:<base64_encoded_data>"
    """
    
    @classmethod
    def new(cls, **kwargs) -> str:
        """Create compact callback data."""
        if not hasattr(cls, 'prefix'):
            raise ValueError(f"CallbackData subclass must define 'prefix'")
        
        # Encode as JSON then base64
        json_data = ""
        for key, value in kwargs.items():
            json_data += f"{key}={value};"
        
        # Remove trailing semicolon
        json_data = json_data.rstrip(';')
        
        # Base64 encode
        encoded = base64.urlsafe_b64encode(json_data.encode('utf-8')).decode('utf-8')
        
        result = f"{cls.prefix}:{encoded}"
        if len(result) > 64:
            raise ValueError(f"Callback data too long: {len(result)} bytes (max 64)")
        
        return result
    
    @classmethod
    def parse(cls, data: str) -> Dict[str, Any]:
        """Parse compact callback data."""
        parts = data.split(":", 1)
        
        if parts[0] != cls.prefix:
            raise ValueError(f"Invalid prefix: {parts[0]}")
        
        if len(parts) < 2:
            return {}
        
        try:
            decoded = base64.urlsafe_b64decode(parts[1]).decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decode callback data: {e}")
        
        result = {}
        for pair in decoded.split(";"):
            if "=" in pair:
                key, value = pair.split("=", 1)
                result[key] = value
        
        return result
