"""
CLI tool for telegram_async - Scaffolding, utilities, and project management
"""
import os
import sys
import json
import shutil
import secrets
import argparse
from pathlib import Path
from typing import Optional, Dict, Any


# ============================================================================
# CLI Commands
# ============================================================================

class CLI:
    """CLI application."""

    def __init__(self):
        self.parser = self._build_parser()

    def _build_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="telegram-async",
            description="telegram_async CLI - Scaffold projects and utilities"
        )
        subparsers = parser.add_subparsers(dest="command", help="Available commands")

        # ---- init ----
        p_init = subparsers.add_parser("init", help="Scaffold a new bot project")
        p_init.add_argument("name", help="Project name")
        p_init.add_argument("path", nargs="?", default=None, help="Target directory (default: current)")
        p_init.add_argument("-t", "--template", choices=["minimal", "standard", "advanced"], default="standard",
                            help="Project template (default: standard)")
        p_init.add_argument("--no-gitignore", action="store_true", help="Skip .gitignore generation")

        # ---- add-handler ----
        p_handler = subparsers.add_parser("add-handler", help="Add a new handler file")
        p_handler.add_argument("name", help="Handler name (e.g. admin, settings)")
        p_handler.add_argument("project", nargs="?", default=".", help="Project root")
        p_handler.add_argument("--with-keyboard", action="store_true", help="Also generate a keyboard builder")

        # ---- add-middleware ----
        p_mw = subparsers.add_parser("add-middleware", help="Add a new middleware file")
        p_mw.add_argument("name", help="Middleware name (e.g. throttling, auth)")
        p_mw.add_argument("project", nargs="?", default=".", help="Project root")

        # ---- generate-token ----
        p_token = subparsers.add_parser("generate-token", help="Generate a secure webhook secret token")
        p_token.add_argument("-l", "--length", type=int, default=32, help="Token length (default: 32)")

        # ---- generate-env ----
        p_env = subparsers.add_parser("generate-env", help="Generate .env from .env.example or template")
        p_env.add_argument("project", nargs="?", default=".", help="Project root")
        p_env.add_argument("--token", help="Set BOT_TOKEN directly")

        # ---- list-templates ----
        subparsers.add_parser("list-templates", help="List available project templates")

        return parser

    def run(self, args=None):
        parsed = self.parser.parse_args(args)
        if not parsed.command:
            self.parser.print_help()
            sys.exit(1)

        commands = {
            "init": self._cmd_init,
            "add-handler": self._cmd_add_handler,
            "add-middleware": self._cmd_add_middleware,
            "generate-token": self._cmd_generate_token,
            "generate-env": self._cmd_generate_env,
            "list-templates": self._cmd_list_templates,
        }

        handler = commands.get(parsed.command)
        if handler:
            success = handler(parsed)
            sys.exit(0 if success else 1)
        else:
            print(f"Unknown command: {parsed.command}")
            sys.exit(1)

    # ===================== init =====================
    def _cmd_init(self, args) -> bool:
        template_name = args.template
        base_path = Path(args.path) if args.path else Path.cwd()
        project_path = base_path / args.name

        if project_path.exists():
            print(f"Directory already exists: {project_path}")
            return False

        print(f"Creating project '{args.name}' with template '{template_name}'...")

        # Define template structures
        templates = {
            "minimal": {
                "dirs": [],
                "files": {
                    "__init__.py": f"# {args.name}\n",
                    "bot.py": self._minimal_bot_py(),
                    "config.py": self._config_py(),
                    "requirements.txt": "telegram-async>=3.2\naiohttp>=3.8.0\npython-dotenv>=0.19.0\n",
                    ".env.example": "BOT_TOKEN=your_token_here\n",
                    ".gitignore": "__pycache__/\n*.pyc\n.env\nvenv/\n.venv/\n",
                    "README.md": self._readme_md(args.name),
                }
            },
            "standard": {
                "dirs": ["handlers", "middlewares", "keyboards"],
                "files": {
                    "__init__.py": f"# {args.name}\n",
                    "bot.py": self._standard_bot_py(),
                    "config.py": self._config_py(),
                    "requirements.txt": "telegram-async>=3.2\naiohttp>=3.8.0\npython-dotenv>=0.19.0\n",
                    ".env.example": "BOT_TOKEN=your_token_here\nLOG_LEVEL=INFO\n",
                    ".gitignore": "__pycache__/\n*.pyc\n.env\nvenv/\n.venv/\n",
                    "README.md": self._readme_md(args.name),
                    "handlers/__init__.py": "from . import start\n\n__all__ = [\"start\"]\n",
                    "handlers/start.py": self._start_handler_py(),
                    "middlewares/__init__.py": "",
                    "keyboards/__init__.py": "from .main import MainKeyboard\n\n__all__ = [\"MainKeyboard\"]\n",
                    "keyboards/main.py": self._main_keyboard_py(),
                    "run.py": self._run_py(),
                }
            },
            "advanced": {
                "dirs": ["handlers", "middlewares", "keyboards", "locales", "tests", "services"],
                "files": {
                    "__init__.py": f"# {args.name}\n",
                    "bot.py": self._advanced_bot_py(),
                    "config.py": self._config_py(),
                    "requirements.txt": "telegram-async>=3.2\naiohttp>=3.8.0\npython-dotenv>=0.19.0\nredis>=4.0.0\npytest>=7.0.0\npytest-asyncio>=0.21.0\n",
                    ".env.example": "BOT_TOKEN=your_token_here\nLOG_LEVEL=INFO\nREDIS_URL=redis://localhost:6379\nDEFAULT_LOCALE=en\n",
                    ".gitignore": "__pycache__/\n*.pyc\n.env\nvenv/\n.venv/\n.pytest_cache/\n",
                    "README.md": self._readme_md(args.name),
                    "handlers/__init__.py": "from . import start\nfrom . import admin\n\n__all__ = [\"start\", \"admin\"]\n",
                    "handlers/start.py": self._start_handler_py(),
                    "handlers/admin.py": self._admin_handler_py(),
                    "middlewares/__init__.py": "from .logging import LoggingMiddleware\n\n__all__ = [\"LoggingMiddleware\"]\n",
                    "middlewares/logging.py": self._logging_middleware_py(),
                    "keyboards/__init__.py": "from .main import MainKeyboard\n\n__all__ = [\"MainKeyboard\"]\n",
                    "keyboards/main.py": self._main_keyboard_py(),
                    "locales/en.json": '{\n  "greeting": "Hello, $name!",\n  "help_text": "Available commands: /start, /help, /settings"\n}\n',
                    "locales/pl.json": '{\n  "greeting": "Cześć, $name!",\n  "help_text": "Dostępne komendy: /start, /help, /settings"\n}\n',
                    "tests/__init__.py": "",
                    "tests/test_start.py": self._test_start_py(),
                    "services/__init__.py": "",
                    "run.py": self._run_py(),
                    "pytest.ini": "[pytest]\nasyncio_mode = auto\n",
                }
            }
        }

        template = templates.get(template_name)
        if not template:
            print(f"Unknown template: {template_name}")
            return False

        # Create directories
        dirs_to_create = [project_path]
        for d in template.get("dirs", []):
            dirs_to_create.append(project_path / d)

        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {dir_path.relative_to(base_path)}")

        # Create files
        for rel_path, content in template.get("files", {}).items():
            if args.no_gitignore and rel_path == ".gitignore":
                continue

            file_path = project_path / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Created: {file_path.relative_to(base_path)}")

        has_run = "run.py" in template.get("files", {})
        print(f"\nProject '{args.name}' created successfully!")
        print(f"\nNext steps:")
        print(f"  cd {args.name}")
        print(f"  pip install -r requirements.txt")
        print(f"  cp .env.example .env  # and set BOT_TOKEN")
        print(f"  python run.py" if has_run else f"  python bot.py")
        return True

    # ===================== add-handler =====================
    def _cmd_add_handler(self, args) -> bool:
        project = Path(args.project)
        handlers_dir = project / "handlers"

        if not handlers_dir.exists():
            handlers_dir.mkdir(parents=True, exist_ok=True)
            init_file = handlers_dir / "__init__.py"
            init_file.write_text(f"from . import {args.name}\n\n__all__ = [\"{args.name}\"]\n")
            print(f"  Created handlers/ directory")

        handler_file = handlers_dir / f"{args.name}.py"
        if handler_file.exists():
            print(f"Handler already exists: {handler_file}")
            return False

        class_name = args.name.capitalize().replace("_", "")
        content = f'''"""
{args.name} handler
"""
from telegram_async.dispatcher import Router
from telegram_async.dispatcher.context import Context

router = Router("{args.name}")

@router.command("{args.name}")
async def cmd_{args.name}(ctx: Context):
    """Handle /{args.name} command"""
    await ctx.reply("{args.name} handler")
'''
        handler_file.write_text(content, encoding='utf-8')
        print(f"  Created handlers/{args.name}.py")

        # Update __init__.py if it exists
        init_file = handlers_dir / "__init__.py"
        if init_file.exists():
            text = init_file.read_text(encoding='utf-8')
            if f"import {args.name}" not in text:
                lines = text.split('\n')
                last_import_idx = 0
                for i, line in enumerate(lines):
                    if line.startswith("from . import") or line.startswith("import "):
                        last_import_idx = i
                lines.insert(last_import_idx + 1, f"from . import {args.name}")

                if "__all__" in text:
                    text = text.replace("__all__ = [", f"__all__ = [\"{args.name}\", ")
                    text = text.replace("__all__=[", f"__all__=[\"{args.name}\", ")
                    lines = text.split('\n')
                else:
                    lines.append(f"")
                    lines.append(f"__all__ = [\"{args.name}\"]")

                init_file.write_text('\n'.join(lines), encoding='utf-8')
                print(f"  Updated handlers/__init__.py")

        # Generate keyboard if requested
        if args.with_keyboard:
            keyboards_dir = project / "keyboards"
            keyboards_dir.mkdir(parents=True, exist_ok=True)
            kb_file = keyboards_dir / f"{args.name}.py"
            if not kb_file.exists():
                kb_content = f'''"""
{args.name} keyboard
"""
from telegram_async.keyboards import InlineKeyboardMarkup, InlineKeyboardButton

class {class_name}Keyboard:
    @staticmethod
    def menu() -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton("Option 1", callback_data="{args.name}_opt1"),
            InlineKeyboardButton("Option 2", callback_data="{args.name}_opt2")
        )
        return keyboard
'''
                kb_file.write_text(kb_content, encoding='utf-8')
                print(f"  Created keyboards/{args.name}.py")

        return True

    # ===================== add-middleware =====================
    def _cmd_add_middleware(self, args) -> bool:
        project = Path(args.project)
        mw_dir = project / "middlewares"

        if not mw_dir.exists():
            mw_dir.mkdir(parents=True, exist_ok=True)
            class_name = args.name.capitalize().replace("_", "")
            init_file = mw_dir / "__init__.py"
            init_file.write_text(f"from .{args.name} import {class_name}Middleware\n\n__all__ = [\"{class_name}Middleware\"]\n")
            print(f"  Created middlewares/ directory")

        mw_file = mw_dir / f"{args.name}.py"
        if mw_file.exists():
            print(f"Middleware already exists: {mw_file}")
            return False

        class_name = args.name.capitalize().replace("_", "")
        content = f'''"""
{args.name} middleware
"""
import logging
import time

logger = logging.getLogger(__name__)


class {class_name}Middleware:
    """{class_name} middleware"""

    async def __call__(self, handler, event, data):
        start_time = time.time()
        logger.info("[{args.name}] Processing update")

        result = await handler(event, data)

        duration = time.time() - start_time
        logger.info(f"[{args.name}] Update processed in {{duration:.3f}}s")

        return result
'''
        mw_file.write_text(content, encoding='utf-8')
        print(f"  Created middlewares/{args.name}.py")

        # Update __init__.py
        init_file = mw_dir / "__init__.py"
        if init_file.exists():
            text = init_file.read_text(encoding='utf-8')
            if f"import {args.name}" not in text and class_name not in text:
                lines = text.split('\n')
                lines.insert(0, f"from .{args.name} import {class_name}Middleware")
                if "__all__" in text:
                    text = text.replace("__all__ = [", f"__all__ = [\"{class_name}Middleware\", ")
                    lines = text.split('\n')
                else:
                    lines.append(f"")
                    lines.append(f"__all__ = [\"{class_name}Middleware\"]")
                init_file.write_text('\n'.join(lines), encoding='utf-8')
                print(f"  Updated middlewares/__init__.py")

        return True

    # ===================== generate-token =====================
    def _cmd_generate_token(self, args) -> bool:
        token = secrets.token_urlsafe(args.length)
        print(token)
        return True

    # ===================== generate-env =====================
    def _cmd_generate_env(self, args) -> bool:
        project = Path(args.project)
        env_file = project / ".env"
        example_file = project / ".env.example"

        if example_file.exists():
            shutil.copy(example_file, env_file)
            print(f"  Copied .env.example -> .env")
        else:
            token = args.token or "YOUR_BOT_TOKEN_HERE"
            content = f"BOT_TOKEN={token}\nLOG_LEVEL=INFO\nDEFAULT_LOCALE=en\nREDIS_URL=redis://localhost:6379\n"
            env_file.write_text(content, encoding='utf-8')
            print(f"  Created .env")

        # Always apply token if provided
        if args.token:
            text = env_file.read_text(encoding='utf-8')
            # Replace any token value after BOT_TOKEN=
            lines = text.split('\n')
            new_lines = []
            for line in lines:
                if line.startswith("BOT_TOKEN="):
                    new_lines.append(f"BOT_TOKEN={args.token}")
                else:
                    new_lines.append(line)
            env_file.write_text('\n'.join(new_lines), encoding='utf-8')
            print(f"  Set BOT_TOKEN in .env")

        print(f"\nRemember to edit .env with your actual values!")
        print(f"  And NEVER commit .env to git!")
        return True

    # ===================== list-templates =====================
    def _cmd_list_templates(self, args) -> bool:
        print("Available project templates:\n")
        print(f"  {'minimal':<12} Minimal bot with single file")
        print(f"  {'standard':<12} Standard bot with handlers, middlewares, keyboards")
        print(f"  {'advanced':<12} Advanced bot with FSM, i18n, metrics, broadcast, testing")
        print()
        return True

    # ===================== Template file generators =====================

    def _minimal_bot_py(self):
        return '''\
"""
Minimal bot
"""
import asyncio
import logging
from telegram_async import Bot, Dispatcher
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

@dp.command("start")
async def cmd_start(ctx):
    await ctx.reply("Hello! I am a bot.")

@dp.message()
async def echo(ctx):
    if ctx.text:
        await ctx.reply(f"You said: {ctx.text}")

async def main():
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
'''

    def _standard_bot_py(self):
        return '''\
"""
Main bot module
"""
import asyncio
import logging
from telegram_async import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import start as start_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

dp.include_router(start_handler.router)

async def main():
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
'''

    def _advanced_bot_py(self):
        return '''\
"""
Advanced bot with FSM, i18n, metrics, background tasks
"""
import asyncio
import logging
import os
from telegram_async import Bot, Dispatcher, Router
from telegram_async.utils import I18n, BotMetrics, BackgroundTasksManager
from config import BOT_TOKEN, REDIS_URL, DEFAULT_LOCALE
from handlers import start as start_handler, admin as admin_handler
from middlewares import LoggingMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

# i18n
i18n = I18n(locales_dir="./locales", default_locale=DEFAULT_LOCALE)

# Metrics
metrics = BotMetrics()

# Background tasks
bg = BackgroundTasksManager()

async def monitor_uptime():
    while True:
        metrics.update_uptime()
        await asyncio.sleep(60)

# Include routers
dp.include_router(start_handler.router)
dp.include_router(admin_handler.router)

async def on_startup():
    logger.info("Bot starting up...")
    await bg.start_all()

async def on_shutdown():
    logger.info("Bot shutting down...")
    await bg.stop_all()

async def main():
    await on_startup()
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
'''

    def _config_py(self):
        return '''\
"""
Configuration
"""
import os

# Bot token from @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Optional: Redis URL for FSM
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Default locale
DEFAULT_LOCALE = os.getenv("DEFAULT_LOCALE", "en")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
'''

    def _start_handler_py(self):
        return '''\
"""
/start handler
"""
from telegram_async.dispatcher import Router
from telegram_async.dispatcher.context import Context

router = Router("start")

@router.command("start")
async def cmd_start(ctx: Context):
    """Handle /start command"""
    user = ctx.update.message.from_user
    await ctx.reply(f"Hello, {user.first_name}! Use /help for commands.")

@router.message()
async def echo_message(ctx: Context):
    """Echo all messages"""
    if ctx.text:
        await ctx.reply(f"You said: {ctx.text}")
'''

    def _admin_handler_py(self):
        return '''\
"""
Admin handlers
"""
from telegram_async.dispatcher import Router
from telegram_async.dispatcher.context import Context

router = Router("admin")

ADMIN_IDS = {123456789}  # Replace with your user ID

async def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

@router.command("admin")
async def cmd_admin(ctx: Context):
    """Admin panel"""
    if not await is_admin(ctx.user_id):
        await ctx.reply("Access denied")
        return
    await ctx.reply("Admin panel")
'''

    def _logging_middleware_py(self):
        return '''\
"""
Logging middleware
"""
import logging
import time

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    """Log all updates"""

    async def __call__(self, handler, event, data):
        start_time = time.time()
        logger.info("Processing update")
        result = await handler(event, data)
        duration = time.time() - start_time
        logger.info(f"Update processed in {duration:.3f}s")
        return result
'''

    def _main_keyboard_py(self):
        return '''\
"""
Main keyboard
"""
from telegram_async.keyboards import InlineKeyboardMarkup, InlineKeyboardButton

class MainKeyboard:
    @staticmethod
    def start_menu() -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton("Help", callback_data="help"),
            InlineKeyboardButton("Stats", callback_data="stats")
        )
        return keyboard
'''

    def _run_py(self):
        return '''\
"""
Entry point
"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from bot import main

if __name__ == "__main__":
    asyncio.run(main())
'''

    def _test_start_py(self):
        return '''\
"""
Tests for start handler
"""
import pytest
from telegram_async.utils import MockBot, MockContext


@pytest.mark.asyncio
async def test_cmd_start():
    from handlers.start import cmd_start

    bot = MockBot()
    ctx = MockContext(user_id=123, chat_id=456, text="/start")

    # This is a minimal test placeholder
    assert ctx.user_id == 123
    assert ctx.chat_id == 456
'''

    def _readme_md(self, name):
        return f'''\
# {name}

Telegram bot built with [telegram-async](https://github.com/your-org/telegram-async)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your bot token:
   ```bash
   cp .env.example .env
   # Edit .env with your BOT_TOKEN
   ```

3. Run the bot:
   ```bash
   python run.py
   # or for minimal:
   python bot.py
   ```

## Structure

- `bot.py` - Main bot setup
- `handlers/` - Message and command handlers
- `middlewares/` - Custom middlewares
- `keyboards/` - Keyboard builders
- `config.py` - Configuration

## Commands

- `/start` - Start the bot
- `/help` - Show help
'''


def main():
    """CLI entry point."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
