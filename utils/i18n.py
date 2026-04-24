"""
i18n/L10n support for telegram_async
"""
import os
import json
import logging
from typing import Dict, Optional, Any, List
from pathlib import Path
from string import Template

logger = logging.getLogger(__name__)


class I18nStorage:
    """Abstract storage backend for translations."""
    
    async def get_translations(self, locale: str) -> Dict[str, str]:
        raise NotImplementedError


class FileStorage(I18nStorage):
    """File-based translation storage."""
    
    def __init__(self, locales_dir: str):
        self.locales_dir = Path(locales_dir)
        self._cache: Dict[str, Dict[str, str]] = {}
    
    async def get_translations(self, locale: str) -> Dict[str, str]:
        if locale in self._cache:
            return self._cache[locale]
        
        locale_file = self.locales_dir / f"{locale}.json"
        if not locale_file.exists():
            logger.warning(f"Locale file not found: {locale_file}")
            return {}
        
        try:
            with open(locale_file, 'r', encoding='utf-8') as f:
                translations = json.load(f)
            self._cache[locale] = translations
            return translations
        except Exception as e:
            logger.error(f"Error loading locale {locale}: {e}")
            return {}


class I18n:
    """
    Internationalization (i18n) manager.
    
    Usage:
        i18n = I18n(locales_dir="./locales", default_locale="en")
        
        # In handler:
        text = await i18n.get(user_locale, "greeting", name="World")
        # Returns: "Hello, World!" if locale has that translation
    """
    
    def __init__(
        self,
        locales_dir: Optional[str] = None,
        default_locale: str = "en",
        storage: Optional[I18nStorage] = None
    ):
        self.default_locale = default_locale
        self.storage = storage or FileStorage(locales_dir) if locales_dir else None
        self._translations: Dict[str, Dict[str, str]] = {}
        self._user_locales: Dict[int, str] = {}
    
    async def load_locale(self, locale: str) -> Dict[str, str]:
        """Load translations for a locale."""
        if locale not in self._translations:
            if self.storage:
                self._translations[locale] = await self.storage.get_translations(locale)
            else:
                self._translations[locale] = {}
        return self._translations[locale]
    
    async def get(
        self,
        locale: str,
        key: str,
        default: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Get translated string.
        
        Args:
            locale: User locale (e.g., "en", "pl")
            key: Translation key
            default: Default value if not found
            **kwargs: Template variables
            
        Returns:
            Translated string
        """
        translations = await self.load_locale(locale)
        text = translations.get(key, default or key)
        
        if kwargs:
            try:
                text = Template(text).safe_substitute(kwargs)
            except Exception:
                pass
        
        return text
    
    def set_user_locale(self, user_id: int, locale: str):
        """Set user's preferred locale."""
        self._user_locales[user_id] = locale
    
    def get_user_locale(self, user_id: int) -> str:
        """Get user's preferred locale."""
        return self._user_locales.get(user_id, self.default_locale)
    
    async def t(self, user_id: int, key: str, default: Optional[str] = None, **kwargs) -> str:
        """
        Get translation for user.
        
        Args:
            user_id: User ID
            key: Translation key
            default: Default value
            **kwargs: Template variables
        """
        locale = self.get_user_locale(user_id)
        return await self.get(locale, key, default, **kwargs)
    
    def get_available_locales(self) -> List[str]:
        """Get list of available locales (file storage only)."""
        if not self.storage or not isinstance(self.storage, FileStorage):
            return [self.default_locale]
        
        if not self.storage.locales_dir.exists():
            return [self.default_locale]
        
        return [
            f.stem for f in self.storage.locales_dir.glob("*.json")
            if f.is_file()
        ]


class gettext:
    """
    Decorator-based translation helper.
    
    Usage:
        _ = gettext(i18n, "en")
        text = _("greeting", name="World")
    """
    
    def __init__(self, i18n: I18n, locale: str):
        self.i18n = i18n
        self.locale = locale
    
    async def __call__(self, key: str, **kwargs) -> str:
        return await self.i18n.get(self.locale, key, **kwargs)
