# client.py - zaktualizowana wersja z retry
import aiohttp
import asyncio
import json
import logging
from typing import Optional, Dict, Any, Union, List
from .exceptions import (
    handle_telegram_error, RateLimitError, NetworkError,
    TelegramAPIError, TimeoutError
)

logger = logging.getLogger(__name__)


class TelegramClient:
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

                # Czekaj tyle ile mówi Telegram
                wait_time = e.retry_after
                logger.warning(f"Rate limited. Waiting {wait_time}s (attempt {attempt + 1}/{self.retry_count})")
                await asyncio.sleep(wait_time)
                self.stats['retried_requests'] += 1

            except NetworkError as e:
                if attempt == self.retry_count:
                    logger.error(f"Network error after {self.retry_count} retries: {e}")
                    raise

                # Exponential backoff
                wait_time = self.retry_delay * (2 ** attempt)
                logger.warning(f"Network error: {e}. Retrying in {wait_time}s")
                await asyncio.sleep(wait_time)
                self.stats['retried_requests'] += 1

            except TelegramAPIError as e:
                # Błędy API nie są ponawiane (poza 429)
                if e.code in [400, 401, 403, 404]:
                    raise
                # Inne błędy API ponawiamy
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
                # Multipart form data dla plików
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
                # JSON data
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

    # === METODY API ===

    async def get_updates(
            self,
            offset: Optional[int] = None,
            limit: int = 100,
            timeout: int = 0,
            allowed_updates: Optional[List[str]] = None
    ) -> List[Dict]:
        """Pobiera aktualizacje z Telegram API"""
        data = {
            'offset': offset,
            'limit': limit,
            'timeout': timeout,
            'allowed_updates': allowed_updates
        }
        return await self._request('getUpdates', data)

    async def send_message(
            self,
            chat_id: Union[int, str],
            text: str,
            parse_mode: Optional[str] = None,
            reply_markup: Optional[Dict] = None,
            disable_web_page_preview: bool = False,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła wiadomość"""
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification,
            'reply_to_message_id': reply_to_message_id
        }
        return await self._request('sendMessage', data)

    async def send_photo(
            self,
            chat_id: Union[int, str],
            photo: Union[str, bytes],
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            reply_markup: Optional[Dict] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła zdjęcie"""
        data = {'chat_id': chat_id}

        if isinstance(photo, str):
            data['photo'] = photo
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if reply_markup:
                data['reply_markup'] = reply_markup
            if disable_notification:
                data['disable_notification'] = disable_notification
            if reply_to_message_id:
                data['reply_to_message_id'] = reply_to_message_id
            return await self._request('sendPhoto', data)
        else:
            # Wysyłanie pliku
            files = {'photo': ('photo.jpg', photo, 'image/jpeg')}
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
            if disable_notification:
                data['disable_notification'] = str(disable_notification)
            if reply_to_message_id:
                data['reply_to_message_id'] = str(reply_to_message_id)
            return await self._request('sendPhoto', data, files)

    async def send_document(
            self,
            chat_id: Union[int, str],
            document: Union[str, bytes],
            filename: Optional[str] = None,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            reply_markup: Optional[Dict] = None,
            disable_notification: bool = False,
            reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Wysyła dokument"""
        data = {'chat_id': chat_id}

        if isinstance(document, str):
            data['document'] = document
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if reply_markup:
                data['reply_markup'] = reply_markup
            if disable_notification:
                data['disable_notification'] = disable_notification
            if reply_to_message_id:
                data['reply_to_message_id'] = reply_to_message_id
            return await self._request('sendDocument', data)
        else:
            files = {'document': (filename or 'document.bin', document, 'application/octet-stream')}
            if caption:
                data['caption'] = caption
            if parse_mode:
                data['parse_mode'] = parse_mode
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
            if disable_notification:
                data['disable_notification'] = str(disable_notification)
            if reply_to_message_id:
                data['reply_to_message_id'] = str(reply_to_message_id)
            return await self._request('sendDocument', data, files)

    async def answer_callback_query(
            self,
            callback_query_id: str,
            text: Optional[str] = None,
            show_alert: bool = False,
            url: Optional[str] = None,
            cache_time: int = 0
    ) -> Dict:
        """Odpowiada na callback query"""
        data = {
            'callback_query_id': callback_query_id,
            'text': text,
            'show_alert': show_alert,
            'url': url,
            'cache_time': cache_time
        }
        return await self._request('answerCallbackQuery', data)

    async def edit_message_text(
            self,
            text: str,
            chat_id: Optional[Union[int, str]] = None,
            message_id: Optional[int] = None,
            inline_message_id: Optional[str] = None,
            parse_mode: Optional[str] = None,
            reply_markup: Optional[Dict] = None,
            disable_web_page_preview: bool = False
    ) -> Dict:
        """Edytuje wiadomość"""
        data = {
            'text': text,
            'parse_mode': parse_mode,
            'reply_markup': reply_markup,
            'disable_web_page_preview': disable_web_page_preview
        }

        if chat_id and message_id:
            data['chat_id'] = chat_id
            data['message_id'] = message_id
        elif inline_message_id:
            data['inline_message_id'] = inline_message_id
        else:
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided")

        return await self._request('editMessageText', data)

    async def get_file(self, file_id: str) -> Dict:
        """Pobiera informacje o pliku"""
        return await self._request('getFile', {'file_id': file_id})

    async def download_file(self, file_path: str) -> bytes:
        """Pobiera plik z serwera Telegram"""
        session = await self._get_session()
        url = f"{self.file_url}/{file_path}"

        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.read()
                raise TelegramAPIError(f"Failed to download file: {resp.status}")
        except aiohttp.ClientError as e:
            raise NetworkError(f"Download failed: {e}")

    async def set_webhook(
            self,
            url: str,
            certificate: Optional[bytes] = None,
            max_connections: int = 40,
            allowed_updates: Optional[List[str]] = None,
            ip_address: Optional[str] = None,
            drop_pending_updates: bool = False,
            secret_token: Optional[str] = None
    ) -> Dict:
        """Ustawia webhook"""
        data = {
            'url': url,
            'max_connections': max_connections,
            'allowed_updates': allowed_updates,
            'ip_address': ip_address,
            'drop_pending_updates': drop_pending_updates,
            'secret_token': secret_token
        }

        if certificate:
            files = {'certificate': ('cert.pem', certificate, 'application/x-pem-file')}
            return await self._request('setWebhook', data, files)

        return await self._request('setWebhook', data)

    async def delete_webhook(self, drop_pending_updates: bool = False) -> Dict:
        """Usuwa webhook"""
        return await self._request('deleteWebhook', {'drop_pending_updates': drop_pending_updates})

    async def get_webhook_info(self) -> Dict:
        """Pobiera informacje o webhooku"""
        return await self._request('getWebhookInfo', {})

    async def get_me(self) -> Dict:
        """Pobiera informacje o bocie"""
        return await self._request('getMe', {})

    async def close(self):
        """Zamyka sesję"""
        if self._session and not self._session.closed:
            await self._session.close()
            logger.debug("Session closed")

    def get_stats(self) -> Dict:
        """Zwraca statystyki klienta"""
        return self.stats.copy()