"""
Obsługa webhooków dla telegram_async
"""
import ssl
import json
import logging
from typing import Optional, Callable, Dict, Any
from aiohttp import web

from ..telegram_types import Update
from ..exceptions import WebhookError

logger = logging.getLogger(__name__)


class WebhookServer:
    """
    Serwer webhook dla Telegram Bota

    Przykład:
        server = WebhookServer(dispatcher, bot)
        await server.set_webhook("https://example.com/webhook")
        server.run_ssl(host="0.0.0.0", port=8443,
                      ssl_cert="cert.pem", ssl_key="key.pem")
    """

    def __init__(self, dispatcher, bot, path: str = "/webhook"):
        """
        Args:
            dispatcher: Instancja Dispatcher
            bot: Instancja Bot
            path: Ścieżka webhooka (domyślnie "/webhook")
        """
        self.dispatcher = dispatcher
        self.bot = bot
        self.path = path
        self.app = web.Application()
        self.app.router.add_post(path, self.handle)
        self.app.router.add_get("/health", self.health_check)
        self.app.on_startup.append(self._on_startup)
        self.app.on_shutdown.append(self._on_shutdown)

        self._runner: Optional[web.AppRunner] = None
        self._site: Optional[web.TCPSite] = None
        self._ssl_context: Optional[ssl.SSLContext] = None

        # Hooki
        self.on_update: Optional[Callable] = None
        self.on_error: Optional[Callable] = None

    async def handle(self, request: web.Request) -> web.Response:
        """
        Handler dla przychodzących webhooków
        """
        try:
            if request.method != 'POST':
                return web.Response(status=405, text="Method not allowed")

            if request.content_type != 'application/json':
                return web.Response(status=400, text="Expected application/json")

            try:
                update_data = await request.json()
            except json.JSONDecodeError:
                return web.Response(status=400, text="Invalid JSON")

            logger.debug(f"Received webhook update: {update_data.get('update_id')}")

            if self.on_update:
                await self.on_update(update_data)

            await self.dispatcher.process_update(self.bot, update_data)

            return web.Response(text="OK")

        except Exception as e:
            logger.error(f"Webhook error: {e}")

            if self.on_error:
                await self.on_error(e)

            return web.Response(status=500, text=f"Error: {e}")

    async def health_check(self, request: web.Request) -> web.Response:
        """Endpoint do sprawdzania statusu"""
        return web.json_response({
            "status": "healthy",
            "webhook_path": self.path,
            "ssl_enabled": self._ssl_context is not None
        })

    async def set_webhook(
            self,
            url: str,
            certificate: Optional[str] = None,
            max_connections: int = 40,
            allowed_updates: Optional[list] = None,
            ip_address: Optional[str] = None,
            drop_pending_updates: bool = False,
            secret_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Ustawia webhook w Telegram

        Args:
            url: Pełny URL webhooka (z https jeśli używamy SSL)
            certificate: Ścieżka do pliku certyfikatu (opcjonalnie)
            max_connections: Maksymalna liczba połączeń (1-100)
            allowed_updates: Lista typów aktualizacji do otrzymywania
            ip_address: Adres IP serwera
            drop_pending_updates: Czy usunąć oczekujące aktualizacje
            secret_token: Tajny token do weryfikacji webhooka

        Returns:
            Odpowiedź z Telegram API
        """
        webhook_url = f"{url.rstrip('/')}{self.path}"

        data = {
            'url': webhook_url,
            'max_connections': max_connections,
            'drop_pending_updates': drop_pending_updates
        }

        if allowed_updates:
            data['allowed_updates'] = allowed_updates

        if ip_address:
            data['ip_address'] = ip_address

        if secret_token:
            data['secret_token'] = secret_token

        if certificate:
            with open(certificate, 'rb') as f:
                cert_data = f.read()
            files = {'certificate': ('cert.pem', cert_data, 'application/x-pem-file')}
            return await self.bot._request('setWebhook', data, files)

        return await self.bot._request('setWebhook', data)

    async def delete_webhook(self, drop_pending_updates: bool = False) -> Dict[str, Any]:
        """Usuwa webhook"""
        return await self.bot._request('deleteWebhook', {
            'drop_pending_updates': drop_pending_updates
        })

    async def get_webhook_info(self) -> Dict[str, Any]:
        """Pobiera informacje o aktualnym webhooku"""
        return await self.bot._request('getWebhookInfo', {})

    def setup_ssl(
            self,
            cert_file: str,
            key_file: str,
            ca_file: Optional[str] = None
    ):
        """
        Konfiguruje SSL dla serwera

        Args:
            cert_file: Ścieżka do pliku certyfikatu (.pem)
            key_file: Ścieżka do pliku klucza prywatnego (.key)
            ca_file: Ścieżka do pliku CA (opcjonalnie)
        """
        self._ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self._ssl_context.load_cert_chain(cert_file, key_file)

        if ca_file:
            self._ssl_context.load_verify_locations(ca_file)
            self._ssl_context.verify_mode = ssl.CERT_REQUIRED

        logger.info(f"SSL configured with cert={cert_file}, key={key_file}")

    async def start(
            self,
            host: str = "0.0.0.0",
            port: int = 8080,
            reuse_address: bool = True,
            reuse_port: bool = False
    ):
        """
        Uruchamia serwer (asynchronicznie)

        Args:
            host: Adres do nasłuchiwania
            port: Port do nasłuchiwania
            reuse_address: Pozwala na ponowne użycie adresu
            reuse_port: Pozwala na ponowne użycie portu (Linux)
        """
        self._runner = web.AppRunner(self.app)
        await self._runner.setup()

        self._site = web.TCPSite(
            self._runner,
            host,
            port,
            ssl_context=self._ssl_context,
            reuse_address=reuse_address,
            reuse_port=reuse_port
        )

        await self._site.start()

        protocol = "https" if self._ssl_context else "http"
        logger.info(f"Webhook server started on {protocol}://{host}:{port}{self.path}")

    async def stop(self):
        """Zatrzymuje serwer"""
        if self._runner:
            await self._runner.cleanup()
            logger.info("Webhook server stopped")

    def run(self, host: str = "0.0.0.0", port: int = 8080):
        """
        Uruchamia serwer (blokująco) - dla prostych przypadków
        """
        web.run_app(self.app, host=host, port=port)

    def run_ssl(
            self,
            host: str = "0.0.0.0",
            port: int = 8443,
            ssl_cert: str = "cert.pem",
            ssl_key: str = "key.pem",
            ssl_ca: Optional[str] = None
    ):
        """
        Uruchamia serwer z SSL (blokująco)

        Args:
            host: Adres do nasłuchiwania
            port: Port do nasłuchiwania (domyślnie 8443 dla Telegram)
            ssl_cert: Ścieżka do pliku certyfikatu
            ssl_key: Ścieżka do pliku klucza
            ssl_ca: Ścieżka do pliku CA (opcjonalnie)
        """
        self.setup_ssl(ssl_cert, ssl_key, ssl_ca)
        web.run_app(self.app, host=host, port=port, ssl_context=self._ssl_context)

    async def _on_startup(self, app):
        """Hook wywoływany przy starcie"""
        logger.info("Webhook server starting up")

    async def _on_shutdown(self, app):
        """Hook wywoływany przy zamknięciu"""
        logger.info("Webhook server shutting down")

    @property
    def is_running(self) -> bool:
        """Sprawdza czy serwer działa"""
        return self._runner is not None and self._runner.server is not None