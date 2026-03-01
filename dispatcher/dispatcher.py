import asyncio
import inspect
from typing import Dict, List, Callable, Any, Optional, Union

from ..client import TelegramClient
from ..types import Update, Message, CallbackQuery
from ..fsm import MemoryStorage, FSMContext, State
from .context import Context
from .middleware import MiddlewareManager


class Dispatcher:
    """
    Główny dyspozytor obsługujący logikę bota, middleware oraz stany FSM.
    Wzorowany na architekturze aiogram 3.x.
    """

    def __init__(self):
        # Inicjalizacja struktur danych dla handlerów
        self.handlers: Dict[str, List[Dict]] = {
            'message': [],
            'callback': [],
            'command': {}
        }
        self.middleware_manager = MiddlewareManager()
        self._startup_hooks: List[Callable] = []
        self._shutdown_hooks: List[Callable] = []
        self._running = False

        # Magazyn stanów (FSM) - domyślnie w pamięci RAM
        self.storage = MemoryStorage()

    # --- Dekoratory ---

    def message(self, *filters):
        """Dekorator dla handlerów wiadomości tekstowych i mediów"""

        def decorator(func: Callable):
            self.handlers['message'].append({
                'func': func,
                'filters': filters
            })
            return func

        return decorator

    def command(self, command: str):
        """Dekorator dla handlerów komend (np. /start)"""

        def decorator(func: Callable):
            self.handlers['command'][command] = func
            return func

        return decorator

    def callback(self, *filters):
        """Dekorator dla zdarzeń przycisków inline (CallbackQuery)"""

        def decorator(func: Callable):
            self.handlers['callback'].append({
                'func': func,
                'filters': filters
            })
            return func

        return decorator

    def middleware(self):
        """Dekorator rejestrujący middleware"""

        def decorator(func: Callable):
            self.middleware_manager.add(func)
            return func

        return decorator

    def startup(self):
        def decorator(func: Callable):
            self._startup_hooks.append(func)
            return func

        return decorator

    def shutdown(self):
        def decorator(func: Callable):
            self._shutdown_hooks.append(func)
            return func

        return decorator

    # --- Przetwarzanie Update'ów ---

    async def process_update(self, client: TelegramClient, update_data: Dict):
        """Główna metoda procesująca przychodzące dane z Telegrama"""
        try:
            update = Update.from_dict(update_data)
            ctx = Context(client, update)

            # Wstrzyknięcie FSMContext do obiektu Context
            if ctx.user_id:
                ctx.fsm = FSMContext(self.storage, ctx.user_id)
            else:
                ctx.fsm = None

            # Funkcja uruchamiająca właściwe handlery po przejściu przez middleware
            async def run_handlers():
                if update.message:
                    await self._process_message(ctx)
                elif update.callback_query:
                    await self._process_callback(ctx)

            # Uruchomienie łańcucha middleware
            await self.middleware_manager.run(ctx, run_handlers)

        except Exception as e:
            print(f"❌ Błąd podczas procesowania update: {e}")

    async def _process_message(self, ctx: Context):
        """Logika dopasowania wiadomości do handlera"""
        if not ctx.message:
            return

        # 1. Sprawdzenie komend (priorytet)
        if ctx.message.text and ctx.message.text.startswith('/'):
            cmd = ctx.message.text.split()[0][1:].lower()
            if cmd in self.handlers['command']:
                await self.handlers['command'][cmd](ctx)
                return

        # 2. Pobranie stanu dla potrzeb filtrów
        current_state = await ctx.fsm.get_state() if ctx.fsm else None

        # 3. Przeszukanie handlerów wiadomości
        for h_dict in self.handlers['message']:
            if await self._check_filters(h_dict['filters'], ctx.message, current_state):
                # Wywołanie handlera z przekazaniem kontekstu (ctx)
                await h_dict['func'](ctx)
                return

    async def _process_callback(self, ctx: Context):
        """Logika dopasowania callback query do handlera"""
        if not ctx.callback_query:
            return

        current_state = await ctx.fsm.get_state() if ctx.fsm else None

        for h_dict in self.handlers['callback']:
            if await self._check_filters(h_dict['filters'], ctx.callback_query, current_state):
                await h_dict['func'](ctx)
                return

    async def _check_filters(self, filters: tuple, obj: Union[Message, CallbackQuery],
                             current_state: Optional[str]) -> bool:
        """Weryfikacja wszystkich filtrów przypisanych do handlera"""
        for f in filters:
            # Obsługa filtra stanu (filters.state)
            if hasattr(f, '_state_filter'):
                required = f._state_filter
                # Konwersja obiektu State na string
                if hasattr(required, 'name'):  # State object
                    required = required.name

                if required != current_state:
                    return False

            # Obsługa filtrów będących funkcjami (asynchronicznymi i zwykłymi)
            elif inspect.iscoroutinefunction(f):
                if not await f(obj):
                    return False
            elif callable(f):
                if not f(obj):
                    return False

        return True

    # --- Pętla Główna (Polling) ---

    async def start_polling(self, client: TelegramClient, skip_updates: bool = True):
        """Uruchamia bota w trybie pollingu"""
        print("🤖 Bot wystartował! Naciśnij Ctrl+C aby zatrzymać.")
        self._running = True
        offset = None

        # Uruchomienie hooków startowych
        for hook in self._startup_hooks:
            await hook()

        try:
            if skip_updates:
                updates = await client.get_updates(limit=1)
                if updates:
                    offset = updates[-1]['update_id'] + 1

            while self._running:
                try:
                    updates = await client.get_updates(offset=offset, timeout=30)
                    for update in updates:
                        offset = update['update_id'] + 1
                        # Asynchroniczne procesowanie każdego update'u
                        asyncio.create_task(self.process_update(client, update))

                    await asyncio.sleep(0.05)
                except Exception as e:
                    print(f"⚠️ Błąd w pętli pollingu: {e}")
                    await asyncio.sleep(2)

        except KeyboardInterrupt:
            pass
        finally:
            self._running = False
            for hook in self._shutdown_hooks:
                await hook()
            await client.close()
            print("\n✅ Bot został bezpiecznie wyłączony.")