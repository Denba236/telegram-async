import aiohttp
import asyncio
import json
import logging
from typing import Optional, Dict, Any, Union, List

from ..exceptions import (
    handle_telegram_error, NetworkError, TimeoutError,
    RateLimitError, TelegramAPIError
)
from .methods import TelegramMethods

logger = logging.getLogger(__name__)


class TelegramClient(TelegramMethods):
    """Klient API Telegram z automatycznym ponawianiem"""

    def __init__(
            self,
            token: str,
            retry_count: int = 3,
            retry_delay: float = 1.0,
            timeout: float = 30.0
    ):
        """
        Args:
            token: Token bota
            retry_count: Liczba ponowień przy błędach
            retry_delay: Bazowe opóźnienie między ponowieniami (exponential backoff)
            timeout: Timeout dla zapytań w sekundach
        """
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.file_url = f"https://api.telegram.org/file/bot{token}"
        self._session: Optional[aiohttp.ClientSession] = None

        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.timeout = timeout

        # Statystyki
        self.stats = {
            'total_requests': 0,
            'failed_requests': 0,
            'retried_requests': 0,
            'rate_limited': 0
        }

    async def _get_session(self) -> aiohttp.ClientSession:
        """Pobiera lub tworzy sesję HTTP"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def _request(
            self,
            method: str,
            data: Dict[str, Any],
            files: Optional[Dict] = None
    ) -> Dict:
        """
        Wykonuje zapytanie do API Telegram z automatycznym ponawianiem

        Args:
            method: Metoda API (np. 'sendMessage')
            data: Dane zapytania
            files: Pliki do wysłania (multipart/form-data)

        Returns:
            Odpowiedź z Telegram API
        """
        self.stats['total_requests'] += 1

        for attempt in range(self.retry_count + 1):
            try:
                return await self._make_request(method, data, files)

            except RateLimitError as e:
                self.stats['rate_limited'] += 1
                if attempt == self.retry_count:
                    logger.error(f"Rate limit exceeded after {self.retry_count} retries")
                    raise

                wait_time = e.retry_after
                logger.warning(f"Rate limited. Waiting {wait_time}s (attempt {attempt + 1}/{self.retry_count})")
                await asyncio.sleep(wait_time)
                self.stats['retried_requests'] += 1

            except NetworkError as e:
                if attempt == self.retry_count:
                    logger.error(f"Network error after {self.retry_count} retries: {e}")
                    raise

                wait_time = self.retry_delay * (2 ** attempt)
                logger.warning(f"Network error: {e}. Retrying in {wait_time}s")
                await asyncio.sleep(wait_time)
                self.stats['retried_requests'] += 1

            except TelegramAPIError as e:
                if e.code in [400, 401, 403, 404]:
                    raise
                if attempt == self.retry_count:
                    raise
                await asyncio.sleep(self.retry_delay * (2 ** attempt))
                self.stats['retried_requests'] += 1

        raise Exception(f"Failed after {self.retry_count} attempts")

    async def _make_request(
            self,
            method: str,
            data: Dict[str, Any],
            files: Optional[Dict] = None
    ) -> Dict:
        """Wykonuje pojedyncze zapytanie"""
        session = await self._get_session()
        url = f"{self.base_url}/{method}"

        try:
            if files:
                form_data = aiohttp.FormData()
                for key, value in data.items():
                    if value is not None:
                        form_data.add_field(key, str(value))

                for field_name, file_data in files.items():
                    if isinstance(file_data, tuple):
                        filename, content, content_type = file_data
                        form_data.add_field(
                            field_name,
                            content,
                            filename=filename,
                            content_type=content_type
                        )
                    else:
                        form_data.add_field(field_name, file_data)

                async with session.post(url, data=form_data) as resp:
                    return await self._handle_response(resp)
            else:
                clean_data = {k: v for k, v in data.items() if v is not None}
                async with session.post(url, json=clean_data) as resp:
                    return await self._handle_response(resp)

        except aiohttp.ClientError as e:
            self.stats['failed_requests'] += 1
            raise NetworkError(f"HTTP error: {e}")
        except asyncio.TimeoutError:
            self.stats['failed_requests'] += 1
            raise TimeoutError(f"Request timeout after {self.timeout}s")

    async def _handle_response(self, resp: aiohttp.ClientResponse) -> Dict:
        """Obsługuje odpowiedź z Telegram API"""
        try:
            result = await resp.json()
        except json.JSONDecodeError:
            self.stats['failed_requests'] += 1
            raise TelegramAPIError(f"Invalid JSON response: {await resp.text()}")

        if not result.get('ok'):
            error_desc = result.get('description', 'Unknown error')
            error_code = result.get('error_code')
            error_data = {
                'error_code': error_code,
                'description': error_desc,
                'parameters': result.get('parameters', {})
            }
            raise handle_telegram_error(error_data)

        return result.get('result', {})

    async def close(self):
        """Zamyka sesję"""
        if self._session and not self._session.closed:
            await self._session.close()
            logger.debug("Session closed")

    def get_stats(self) -> Dict:
        """Zwraca statystyki klienta"""
        return self.stats.copy()