"""
CLI tool for telegram_async - Scaffolding, utilities, and project management
"""
import os
import sys
import json
import shutil
import secrets
import argparse
import asyncio
import re
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


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
        p_init.add_argument("--force", action="store_true", help="Overwrite if project exists")
        p_init.add_argument("--git", action="store_true", help="Initialize git repository")
        p_init.add_argument("--docker", action="store_true", help="Include Docker configuration")
        p_init.add_argument("--docker-only", action="store_true", help="Only create Docker files (no full project)")

        # ---- add-handler ----
        p_handler = subparsers.add_parser("add-handler", help="Add a new handler file")
        p_handler.add_argument("name", help="Handler name (e.g. admin, settings)")
        p_handler.add_argument("project", nargs="?", default=".", help="Project root")
        p_handler.add_argument("--with-keyboard", action="store_true", help="Also generate a keyboard builder")
        p_handler.add_argument("--with-tests", action="store_true", help="Generate test file")

        # ---- add-middleware ----
        p_mw = subparsers.add_parser("add-middleware", help="Add a new middleware file")
        p_mw.add_argument("name", help="Middleware name (e.g. throttling, auth)")
        p_mw.add_argument("project", nargs="?", default=".", help="Project root")

        # ---- add-conversation ----
        p_conv = subparsers.add_parser("add-conversation", help="Add a new conversation/wizard handler")
        p_conv.add_argument("name", help="Conversation name (e.g. registration, feedback)")
        p_conv.add_argument("project", nargs="?", default=".", help="Project root")
        p_conv.add_argument("--steps", type=int, default=3, help="Number of conversation steps")
        p_conv.add_argument("--with-cancel", action="store_true", default=True, help="Add cancel state")
        p_conv.add_argument("--storage", choices=["memory", "redis"], default="memory", help="FSM storage backend")

        # ---- add-filter ----
        p_filter = subparsers.add_parser("add-filter", help="Add a new custom filter file")
        p_filter.add_argument("name", help="Filter name (e.g. is_admin, has_text)")
        p_filter.add_argument("project", nargs="?", default=".", help="Project root")
        p_filter.add_argument("--base", choices=["BaseFilter", "TextFilter", "CommandFilter"], default="BaseFilter",
                              help="Filter base class")

        # ---- add-state ----
        p_state = subparsers.add_parser("add-state", help="Add a new FSM state handler")
        p_state.add_argument("name", help="State name (e.g. registration, feedback)")
        p_state.add_argument("project", nargs="?", default=".", help="Project root")
        p_state.add_argument("--steps", type=int, default=2, help="Number of conversation steps")
        p_state.add_argument("--with-cancel", action="store_true", default=True, help="Add cancel state")

        # ---- generate-token ----
        p_token = subparsers.add_parser("generate-token", help="Generate a secure webhook secret token")
        p_token.add_argument("-l", "--length", type=int, default=32, help="Token length (default: 32)")

        # ---- generate-env ----
        p_env = subparsers.add_parser("generate-env", help="Generate .env from .env.example or template")
        p_env.add_argument("project", nargs="?", default=".", help="Project root")
        p_env.add_argument("--token", help="Set BOT_TOKEN directly")

        # ---- validate-env ----
        p_validate = subparsers.add_parser("validate-env", help="Validate .env configuration")
        p_validate.add_argument("project", nargs="?", default=".", help="Project root")
        p_validate.add_argument("--strict", action="store_true", help="Fail on missing optional vars")

        # ---- list-templates ----
        subparsers.add_parser("list-templates", help="List available project templates")

        # ---- list-commands ----
        p_list_cmds = subparsers.add_parser("list-commands", help="List bot commands (from BotFather)")
        p_list_cmds.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")

        # ---- run ----
        p_run = subparsers.add_parser("run", help="Run the bot with polling or webhook mode")
        p_run.add_argument("mode", nargs="?", choices=["polling", "webhook"], default="polling",
                           help="Run mode (default: polling)")
        p_run.add_argument("--host", default="0.0.0.0", help="Webhook host (default: 0.0.0.0)")
        p_run.add_argument("--port", type=int, default=8080, help="Webhook port (default: 8080)")
        p_run.add_argument("--path", default="/webhook", help="Webhook path (default: /webhook)")
        p_run.add_argument("--url", help="Webhook URL (auto-generated if not provided)")
        p_run.add_argument("--cert", help="Path to SSL certificate")
        p_run.add_argument("--key", help="Path to SSL private key")
        p_run.add_argument("--skip-update", action="store_true", help="Skip pending updates on startup")
        p_run.add_argument("-t", "--target", default="bot:main", help="Module:callable target (default: bot:main)")

        # ---- deploy ----
        p_deploy = subparsers.add_parser("deploy", help="Generate deployment configurations")
        p_deploy.add_argument("type", nargs="?", choices=["docker", "systemd", "railway", "render", "fly", "vercel"], default="docker",
                              help="Deployment type (default: docker)")
        p_deploy.add_argument("--project", default=".", help="Project root")
        p_deploy.add_argument("--name", help="Project name (default: directory name)")
        p_deploy.add_argument("--port", type=int, default=8080, help="Port for webhook mode")
        p_deploy.add_argument("--validate", action="store_true", help="Validate before generating")

        # ---- add-webhook ----
        p_webhook = subparsers.add_parser("add-webhook", help="Configure webhook for the bot")
        p_webhook.add_argument("url", help="Full webhook URL")
        p_webhook.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")
        p_webhook.add_argument("--cert", help="Path to SSL certificate")
        p_webhook.add_argument("--secret", help="Secret token for verification")
        p_webhook.add_argument("--max-connections", type=int, default=100, help="Max connections (default: 100)")
        p_webhook.add_argument("--drop-pending", action="store_true", help="Drop pending updates")

        # ---- delete-webhook ----
        p_del_webhook = subparsers.add_parser("delete-webhook", help="Delete bot webhook")
        p_del_webhook.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")
        p_del_webhook.add_argument("--drop-pending", action="store_true", help="Drop all pending updates")

        # ---- get-updates ----
        p_updates = subparsers.add_parser("get-updates", help="Get pending updates (debug)")
        p_updates.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")
        p_updates.add_argument("--offset", type=int, help="Update offset")
        p_updates.add_argument("--limit", type=int, default=100, help="Limit (default: 100)")
        p_updates.add_argument("--timeout", type=int, default=0, help="Timeout in seconds")
        p_updates.add_argument("--json", action="store_true", help="Output as JSON")

        # ---- send-message ----
        p_send = subparsers.add_parser("send-message", help="Send a test message")
        p_send.add_argument("chat_id", help="Target chat ID")
        p_send.add_argument("text", help="Message text")
        p_send.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")
        p_send.add_argument("--parse-mode", choices=["markdown", "html"], help="Parse mode")
        p_send.add_argument("--reply-to", type=int, help="Reply to message ID")
        p_send.add_argument("--keyboard", help="Inline keyboard JSON")

        # ---- set-commands ----
        p_set_cmds = subparsers.add_parser("set-commands", help="Set bot commands")
        p_set_cmds.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")
        p_set_cmds.add_argument("--commands", help="JSON array of commands: [[\"cmd\",\"desc\"],...]")

        # ---- get-chat ----
        p_get_chat = subparsers.add_parser("get-chat", help="Get chat info")
        p_get_chat.add_argument("chat_id", help="Chat ID")
        p_get_chat.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")

        # ---- broadcast ----
        p_broadcast = subparsers.add_parser("broadcast", help="Broadcast message to users")
        p_broadcast.add_argument("text", help="Message text")
        p_broadcast.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")
        p_broadcast.add_argument("--parse-mode", choices=["markdown", "html"], help="Parse mode")
        p_broadcast.add_argument("--chat-ids", help="Comma-separated chat IDs: 123,456,789")
        p_broadcast.add_argument("--file", help="File with chat IDs (one per line)")

        # ---- generate-docs ----
        p_docs = subparsers.add_parser("generate-docs", help="Generate bot API documentation")
        p_docs.add_argument("project", nargs="?", default=".", help="Project root")
        p_docs.add_argument("--output", default="API.md", help="Output file (default: API.md)")
        p_docs.add_argument("--format", choices=["markdown", "html", "json"], default="markdown", help="Output format")

        # ---- backup ----
        p_backup = subparsers.add_parser("backup", help="Backup FSM state")
        p_backup.add_argument("project", nargs="?", default=".", help="Project root")
        p_backup.add_argument("--output", help="Output file (default: backup_YYYYMMDD.json)")

        # ---- migrate ----
        p_migrate = subparsers.add_parser("migrate", help="Migrate template/project version")
        p_migrate.add_argument("project", nargs="?", default=".", help="Project root")
        p_migrate.add_argument("--from-version", help="Source version")
        p_migrate.add_argument("--to-version", default="latest", help="Target version (default: latest)")
        p_migrate.add_argument("--dry-run", action="store_true", help="Show changes without applying")

        # ---- dev ----
        p_dev = subparsers.add_parser("dev", help="Run bot in development mode")
        p_dev.add_argument("--host", default="0.0.0.0", help="Host (default: 0.0.0.0)")
        p_dev.add_argument("--port", type=int, default=8080, help="Port (default: 8080)")
        p_dev.add_argument("--reload", action="store_true", help="Auto-reload on changes")
        p_dev.add_argument("--debug", action="store_true", help="Enable debug mode")
        p_dev.add_argument("-t", "--target", default="bot:main", help="Module:callable target")

        # ---- shell ----
        p_shell = subparsers.add_parser("shell", help="Interactive bot shell")
        p_shell.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")

        # ---- stats ----
        p_stats = subparsers.add_parser("stats", help="Show bot statistics")
        p_stats.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")
        p_stats.add_argument("--json", action="store_true", help="Output as JSON")

        # ---- health ----
        p_health = subparsers.add_parser("health", help="Health check for the bot")
        p_health.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")
        p_health.add_argument("--verbose", action="store_true", help="Verbose output")

        # ---- get-member ----
        p_member = subparsers.add_parser("get-member", help="Get chat member info")
        p_member.add_argument("chat_id", help="Chat ID")
        p_member.add_argument("user_id", help="User ID")
        p_member.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")

        # ---- ban-user ----
        p_ban = subparsers.add_parser("ban-user", help="Ban a user from chat")
        p_ban.add_argument("chat_id", help="Chat ID")
        p_ban.add_argument("user_id", help="User ID to ban")
        p_ban.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")

        # ---- unban-user ----
        p_unban = subparsers.add_parser("unban-user", help="Unban a user from chat")
        p_unban.add_argument("chat_id", help="Chat ID")
        p_unban.add_argument("user_id", help="User ID to unban")
        p_unban.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")

        # ---- pin-message ----
        p_pin = subparsers.add_parser("pin-message", help="Pin a message")
        p_pin.add_argument("chat_id", help="Chat ID")
        p_pin.add_argument("message_id", help="Message ID to pin")
        p_pin.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")
        p_pin.add_argument("--disable-notification", action="store_true", help="Disable notification")

        # ---- unpin-message ----
        p_unpin = subparsers.add_parser("unpin-message", help="Unpin a message")
        p_unpin.add_argument("chat_id", help="Chat ID")
        p_unpin.add_argument("--message-id", type=int, help="Message ID to unpin (or all if not set)")
        p_unpin.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")

        # ---- delete-message ----
        p_delete = subparsers.add_parser("delete-message", help="Delete a message")
        p_delete.add_argument("chat_id", help="Chat ID")
        p_delete.add_argument("message_id", help="Message ID to delete")
        p_delete.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")

        # ---- export-chat ----
        p_export = subparsers.add_parser("export-chat", help="Export chat data")
        p_export.add_argument("chat_id", help="Chat ID")
        p_export.add_argument("--token", help="Bot token (or set BOT_TOKEN env)")
        p_export.add_argument("--output", help="Output file (default: export.json)")

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
            "add-conversation": self._cmd_add_conversation,
            "generate-token": self._cmd_generate_token,
            "generate-env": self._cmd_generate_env,
            "validate-env": self._cmd_validate_env,
            "list-templates": self._cmd_list_templates,
            "list-commands": self._cmd_list_commands,
            "run": self._cmd_run,
            "deploy": self._cmd_deploy,
            "add-filter": self._cmd_add_filter,
            "add-state": self._cmd_add_state,
            "add-webhook": self._cmd_add_webhook,
            "delete-webhook": self._cmd_delete_webhook,
            "get-updates": self._cmd_get_updates,
            "send-message": self._cmd_send_message,
            "set-commands": self._cmd_set_commands,
            "get-chat": self._cmd_get_chat,
            "broadcast": self._cmd_broadcast,
            "generate-docs": self._cmd_generate_docs,
            "backup": self._cmd_backup,
            "migrate": self._cmd_migrate,
            "dev": self._cmd_dev,
            "shell": self._cmd_shell,
            "stats": self._cmd_stats,
            "health": self._cmd_health,
            "get-member": self._cmd_get_member,
            "ban-user": self._cmd_ban_user,
            "unban-user": self._cmd_unban_user,
            "pin-message": self._cmd_pin_message,
            "unpin-message": self._cmd_unpin_message,
            "delete-message": self._cmd_delete_message,
            "export-chat": self._cmd_export_chat,
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
            if args.force:
                print(f"Removing existing project: {project_path}")
                shutil.rmtree(project_path)
            else:
                print(f"Directory already exists: {project_path}")
                print(f"Use --force to overwrite")
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
        
        # Add Docker files if requested
        if args.docker or args.docker_only:
            docker_files = self._generate_docker_files(project_path.name)
            for rel_path, content in docker_files.items():
                file_path = project_path / rel_path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(content, encoding='utf-8')
                print(f"  Created: {file_path.relative_to(base_path)}")
        
        print(f"\nProject '{args.name}' created successfully!")
        print(f"\nNext steps:")
        print(f"  cd {args.name}")
        print(f"  pip install -r requirements.txt")
        print(f"  cp .env.example .env  # and set BOT_TOKEN")
        
        if args.git:
            try:
                subprocess.run(["git", "init"], cwd=project_path, capture_output=True, check=True)
                subprocess.run(["git", "add", "."], cwd=project_path, capture_output=True)
                print(f"  Initialized git repository")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print(f"  Warning: Could not initialize git")
        
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
                if kb_file.exists():
                    pass
                else:
                    kb_file.write_text(kb_content, encoding='utf-8')
                    print(f"  Created keyboards/{args.name}.py")

        # Generate test if requested
        if args.with_tests:
            tests_dir = project / "tests"
            tests_dir.mkdir(parents=True, exist_ok=True)
            test_file = tests_dir / f"test_{args.name}.py"
            if not test_file.exists():
                test_content = f'''"""
Tests for {args.name} handler
"""
import pytest
from telegram_async.utils.testing import MockContext, run_handler_test


@pytest.mark.asyncio
async def test_cmd_{args.name}():
    """Test /{args.name} command"""
    from handlers.{args.name} import cmd_{args.name}
    
    ctx = MockContext(user_id=123, chat_id=456, text="/{args.name}")
    
    # Mock the reply method
    ctx.reply = pytest.AsyncMock()
    
    await cmd_{args.name}(ctx)
    
    ctx.reply.assert_called_once()


@pytest.mark.asyncio
async def test_{args.name}_handler():
    """Test {args.name} message handler"""
    from handlers.{args.name} import echo_{args.name}
    
    ctx = MockContext(user_id=123, chat_id=456, text="test message")
    
    ctx.reply = pytest.AsyncMock()
    
    await echo_{args.name}(ctx)
    
    # Add your assertions
'''
                test_file.write_text(test_content, encoding='utf-8')
                print(f"  Created tests/test_{args.name}.py")
                
                # Ensure tests/__init__.py exists
                init_file = tests_dir / "__init__.py"
                if not init_file.exists():
                    init_file.write_text("", encoding='utf-8')

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

    # ===================== validate-env =====================
    def _cmd_validate_env(self, args) -> bool:
        project = Path(args.project)
        env_file = project / ".env"
        
        if not env_file.exists():
            print(f"[ERROR] .env file not found in {project}")
            return False
        
        print(f"Validating .env configuration...\n")
        
        # Define required and optional variables
        required_vars = ["BOT_TOKEN"]
        optional_vars = ["LOG_LEVEL", "REDIS_URL", "DEFAULT_LOCALE", "WEBHOOK_URL"]
        
        env_vars = {}
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        
        errors = []
        warnings = []
        
        for var in required_vars:
            if var not in env_vars or not env_vars[var]:
                errors.append(f"[ERROR] {var} is required but not set")
            elif env_vars[var] == f"your_{var.lower()}_here" or env_vars[var] == "YOUR_BOT_TOKEN_HERE":
                errors.append(f"[ERROR] {var} has placeholder value")
        
        for var in optional_vars:
            if var not in env_vars:
                warnings.append(f"[WARN] {var} is not set (optional)")
        
        if errors:
            print("Errors found:")
            for e in errors:
                print(f"  {e}")
        
        if warnings and args.strict:
            print("Warnings (strict mode):")
            for w in warnings:
                print(f"  {w}")
            errors.extend(warnings)
        
        if errors:
            print(f"\nValidation FAILED: {len(errors)} issue(s)")
            return False
        
        print("[OK] All required variables are set")
        if warnings:
            print(f"[OK] Optional variables not set: {len(warnings)} (optional)")
        else:
            print("[OK] All optional variables are set")
        
        return True

    # ===================== list-commands =====================
    def _cmd_list_commands(self, args) -> bool:
        import aiohttp
        
        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False
        
        print(f"Fetching bot commands...\n")
        
        async def fetch_commands():
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.telegram.org/bot{token}/getMyCommands") as resp:
                    return await resp.json()
        
        try:
            result = asyncio.run(fetch_commands())
        except Exception as e:
            print(f"[ERROR] Failed to fetch commands: {e}")
            return False
        
        if result.get('ok'):
            commands = result.get('result', [])
            if commands:
                print(f"Bot commands ({len(commands)}):\n")
                for cmd in commands:
                    desc = cmd.get('description', '')
                    cmd_name = cmd.get('command', '')
                    print(f"  /{cmd_name:<20} {desc}")
            else:
                print("No commands set. Use /setcommands in @BotFather")
            return True
        else:
            print(f"[ERROR] {result.get('description', 'Unknown error')}")
            return False

    # ===================== add-conversation =====================
    def _cmd_add_conversation(self, args) -> bool:
        project = Path(args.project)
        handlers_dir = project / "handlers"
        
        if not handlers_dir.exists():
            handlers_dir.mkdir(parents=True, exist_ok=True)
            print(f"  Created handlers/ directory")
        
        conv_file = handlers_dir / f"{args.name}.py"
        if conv_file.exists():
            print(f"Conversation already exists: {conv_file}")
            return False
        
        class_name = args.name.capitalize().replace("_", "")
        steps = args.steps
        storage = args.storage
        with_cancel = args.with_cancel
        
        state_vars = [f"STEP_{i+1}" for i in range(steps)]
        step_handlers = ""
        
        for i in range(steps):
            step_num = i + 1
            step_handlers += f'''
@router.message({class_name}Conv.{state_vars[i]})
async def handle_step{step_num}(ctx: Context):
    """Handle step {step_num}"""
    data = ctx.state.data
    data["step{step_num}"] = ctx.text
    
    if ctx.text and ctx.text.lower() in ("cancel", "/cancel"):
        await ctx.reply("Conversation cancelled.")
        await ctx.state.reset()
        return
    
    # TODO: Process step {step_num} data
    await ctx.reply(f"Step {step_num}: Received '{{ctx.text}}'")
    
    # Move to next step or finish
'''
        
        next_step_code = f"await ctx.state.set_state({class_name}Conv.{state_vars[min(steps-1, i+1)]})" if i < steps-1 else "await ctx.reply('Conversation completed!')"
        step_handlers = step_handlers.rstrip()
        for i in range(steps-1):
            step_handlers += f'''
    {next_step_code.replace(f"STEP_{i+2}", f"STEP_{i+1}") if i == 0 else ""}
'''
        
        # Rebuild step handlers properly
        step_handlers = ""
        for i in range(steps):
            step_num = i + 1
            is_last = i == steps - 1
            next_state = f"{class_name}Conv.{state_vars[i+1]}" if not is_last else "None"
            step_handlers += f'''
@router.message({class_name}Conv.{state_vars[i]})
async def handle_step{step_num}(ctx: Context):
    """Handle step {step_num}"""
    data = ctx.state.data
    data["step{step_num}"] = ctx.text
    
    if ctx.text and ctx.text.lower() in ("cancel", "/cancel"):
        await ctx.reply("Conversation cancelled.")
        await ctx.state.reset()
        return
    
    # TODO: Process step {step_num} data
    await ctx.reply(f"Step {step_num}: Received '{{ctx.text}}'")
'''
            if not is_last:
                step_handlers += f'''    await ctx.state.set_state({class_name}Conv.{state_vars[i+1]})
'''
            else:
                step_handlers += f'''    await ctx.reply("Conversation completed! All steps finished.")
    await ctx.state.reset()
'''
        
        cancel_code = ""
        if with_cancel:
            cancel_code = '''
@router.message()
async def handle_cancel(ctx: Context):
    """Handle cancel command globally"""
    if ctx.text and ctx.text.lower() in ("cancel", "/cancel"):
        await ctx.reply("Use /cancel to cancel a conversation in progress.")
'''
        
        content = f'''"""
{args.name} conversation handler
"""
from telegram_async.dispatcher import Router
from telegram_async.dispatcher.context import Context
from telegram_async.fsm import State, StatesGroup


class {class_name}Conv(StatesGroup):
    """{class_name} conversation states"""
'''
        for var in state_vars:
            content += f"    {var} = State()\n"
        
        content += f'''

router = Router("{args.name}")

@router.command("{args.name}")
async def cmd_{args.name}(ctx: Context):
    """Start {args.name} conversation"""
    await ctx.state.set_state({class_name}Conv.{state_vars[0]})
    await ctx.reply("Starting {args.name} conversation. Step 1:")
{step_handlers}
{cancel_code}
'''
        
        conv_file.write_text(content, encoding='utf-8')
        print(f"  Created handlers/{args.name}.py")
        
        # Update __init__.py
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
                    lines = text.split('\n')
                else:
                    lines.append(f"")
                    lines.append(f"__all__ = [\"{args.name}\"]")
                init_file.write_text('\n'.join(lines), encoding='utf-8')
                print(f"  Updated handlers/__init__.py")
        
        return True

    # ===================== add-webhook =====================
    def _cmd_add_webhook(self, args) -> bool:
        import aiohttp
        
        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False
        
        print(f"Setting webhook to: {args.url}\n")
        
        async def set_webhook():
            data = {"url": args.url}
            if args.cert:
                data["certificate"] = open(args.cert, "rb")
            if args.secret:
                data["secret_token"] = args.secret
            if args.max_connections:
                data["max_connections"] = args.max_connections
            if args.drop_pending:
                data["drop_pending_updates"] = True
            
            async with aiohttp.ClientSession() as session:
                if args.cert:
                    form = aiohttp.FormData()
                    form.add_field("url", args.url)
                    with open(args.cert, 'rb') as f:
                        form.add_field("certificate", f, filename="cert.pem")
                    if args.secret:
                        form.add_field("secret_token", args.secret)
                    async with session.post(f"https://api.telegram.org/bot{token}/setWebhook", data=form) as resp:
                        return await resp.json()
                else:
                    async with session.post(f"https://api.telegram.org/bot{token}/setWebhook", json=data) as resp:
                        return await resp.json()
        
        try:
            result = asyncio.run(set_webhook())
        except Exception as e:
            print(f"[ERROR] Failed to set webhook: {e}")
            return False
        
        if result.get('ok'):
            print("[OK] Webhook set successfully")
            return True
        else:
            print(f"[ERROR] {result.get('description', 'Unknown error')}")
            return False

    # ===================== delete-webhook =====================
    def _cmd_delete_webhook(self, args) -> bool:
        import aiohttp
        
        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False
        
        print("Deleting webhook...\n")
        
        async def delete_webhook():
            data = {}
            if args.drop_pending:
                data["drop_pending_updates"] = True
            async with aiohttp.ClientSession() as session:
                async with session.post(f"https://api.telegram.org/bot{token}/deleteWebhook", json=data) as resp:
                    return await resp.json()
        
        try:
            result = asyncio.run(delete_webhook())
        except Exception as e:
            print(f"[ERROR] Failed to delete webhook: {e}")
            return False
        
        if result.get('ok'):
            print("[OK] Webhook deleted successfully")
            return True
        else:
            print(f"[ERROR] {result.get('description', 'Unknown error')}")
            return False

    # ===================== get-updates =====================
    def _cmd_get_updates(self, args) -> bool:
        import aiohttp
        
        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False
        
        print(f"Getting updates (offset={args.offset}, limit={args.limit})...\n")
        
        async def get_updates():
            data = {"offset": args.offset or -1, "limit": args.limit, "timeout": args.timeout}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.telegram.org/bot{token}/getUpdates", params=data) as resp:
                    return await resp.json()
        
        try:
            result = asyncio.run(get_updates())
        except Exception as e:
            print(f"[ERROR] Failed to get updates: {e}")
            return False
        
        if result.get('ok'):
            updates = result.get('result', [])
            print(f"Found {len(updates)} updates\n")
            
            if args.json:
                print(json.dumps(updates, indent=2, default=str))
            else:
                for i, update in enumerate(updates):
                    update_id = update.get('update_id', '?')
                    msg = update.get('message', {})
                    if msg:
                        text = msg.get('text', '')
                        chat = msg.get('chat', {})
                        print(f"  [{i+1}] ID={update_id} Chat={chat.get('id')} Text={text[:50]}...")
                    else:
                        print(f"  [{i+1}] ID={update_id} (no message)")
            
            if updates:
                print(f"\nLast update_id: {updates[-1].get('update_id')}")
                print(f"Use --offset {updates[-1].get('update_id') + 1} to acknowledge")
            
            return True
        else:
            print(f"[ERROR] {result.get('description', 'Unknown error')}")
            return False

    # ===================== send-message =====================
    def _cmd_send_message(self, args) -> bool:
        import aiohttp
        
        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False
        
        print(f"Sending message to {args.chat_id}...\n")
        
        async def send():
            data = {"chat_id": args.chat_id, "text": args.text}
            if args.parse_mode:
                data["parse_mode"] = args.parse_mode
            if args.reply_to:
                data["reply_to_message_id"] = args.reply_to
            if args.keyboard:
                try:
                    keyboard = json.loads(args.keyboard)
                    data["reply_markup"] = keyboard
                except json.JSONDecodeError:
                    print("[ERROR] Invalid keyboard JSON")
                    return None
            
            async with aiohttp.ClientSession() as session:
                async with session.post(f"https://api.telegram.org/bot{token}/sendMessage", json=data) as resp:
                    return await resp.json()
        
        try:
            result = asyncio.run(send())
        except Exception as e:
            print(f"[ERROR] Failed to send message: {e}")
            return False
        
        if result is None:
            return False
        
        if result.get('ok'):
            msg = result.get('result', {})
            print(f"[OK] Message sent! ID: {msg.get('message_id')}")
            return True
        else:
            print(f"[ERROR] {result.get('description', 'Unknown error')}")
            return False

    # ===================== set-commands =====================
    def _cmd_set_commands(self, args) -> bool:
        import aiohttp
        
        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False
        
        if not args.commands:
            print("[ERROR] --commands required. Example: '[[\"start\",\"Start bot\"],[\"help\",\"Get help\"]]'")
            return False
        
        print(f"Setting bot commands...\n")
        
        try:
            commands = json.loads(args.commands)
        except json.JSONDecodeError:
            print("[ERROR] Invalid JSON format for --commands")
            return False
        
        formatted_commands = []
        for cmd in commands:
            if isinstance(cmd, list) and len(cmd) == 2:
                formatted_commands.append({"command": cmd[0], "description": cmd[1]})
            elif isinstance(cmd, dict):
                formatted_commands.append(cmd)
        
        async def set_commands():
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://api.telegram.org/bot{token}/setMyCommands",
                    json={"commands": formatted_commands}
                ) as resp:
                    return await resp.json()
        
        try:
            result = asyncio.run(set_commands())
        except Exception as e:
            print(f"[ERROR] Failed to set commands: {e}")
            return False
        
        if result.get('ok'):
            print(f"[OK] Set {len(formatted_commands)} commands successfully")
            return True
        else:
            print(f"[ERROR] {result.get('description', 'Unknown error')}")
            return False

    # ===================== get-chat =====================
    def _cmd_get_chat(self, args) -> bool:
        import aiohttp
        
        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False
        
        print(f"Getting chat info for ID: {args.chat_id}...\n")
        
        async def get_chat():
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.telegram.org/bot{token}/getChat",
                    params={"chat_id": args.chat_id}
                ) as resp:
                    return await resp.json()
        
        try:
            result = asyncio.run(get_chat())
        except Exception as e:
            print(f"[ERROR] Failed to get chat: {e}")
            return False
        
        if result.get('ok'):
            chat = result.get('result', {})
            print(f"Chat Information:")
            print(f"  ID: {chat.get('id')}")
            print(f"  Type: {chat.get('type')}")
            print(f"  Title: {chat.get('title', 'N/A')}")
            print(f"  Username: {chat.get('username', 'N/A')}")
            print(f"  First Name: {chat.get('first_name', 'N/A')}")
            print(f"  Description: {chat.get('description', 'N/A')}")
            if chat.get('photo'):
                print(f"  Has Photo: Yes")
            return True
        else:
            print(f"[ERROR] {result.get('description', 'Unknown error')}")
            return False

    # ===================== broadcast =====================
    def _cmd_broadcast(self, args) -> bool:
        import aiohttp
        
        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False
        
        chat_ids = []
        
        # Collect chat IDs from various sources
        if args.chat_ids:
            try:
                chat_ids = [int(cid.strip()) for cid in args.chat_ids.split(",")]
            except ValueError:
                print("[ERROR] Invalid chat IDs format. Use: 123,456,789")
                return False
        
        if args.file:
            file_path = Path(args.file)
            if file_path.exists():
                with open(file_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            try:
                                chat_ids.append(int(line))
                            except ValueError:
                                pass
        
        if not chat_ids:
            print("[ERROR] No chat IDs. Use --chat-ids '123,456' or --file chat_ids.txt")
            return False
        
        print(f"Broadcasting to {len(chat_ids)} chats...\n")
        
        async def broadcast():
            sent = 0
            failed = 0
            
            async with aiohttp.ClientSession() as session:
                for chat_id in chat_ids:
                    try:
                        data = {"chat_id": chat_id, "text": args.text}
                        if args.parse_mode:
                            data["parse_mode"] = args.parse_mode
                        
                        async with session.post(
                            f"https://api.telegram.org/bot{token}/sendMessage",
                            json=data
                        ) as resp:
                            result = await resp.json()
                            if result.get('ok'):
                                sent += 1
                                print(f"  [OK] Sent to {chat_id}")
                            else:
                                failed += 1
                                print(f"  [FAIL] {chat_id}: {result.get('description', 'Unknown')}")
                    except Exception as e:
                        failed += 1
                        print(f"  [FAIL] {chat_id}: {e}")
            
            return {"sent": sent, "failed": failed}
        
        try:
            result = asyncio.run(broadcast())
        except Exception as e:
            print(f"[ERROR] Failed to broadcast: {e}")
            return False
        
        print(f"\n[OK] Broadcast complete: {result['sent']} sent, {result['failed']} failed")
        return True

    # ===================== generate-docs =====================
    def _cmd_generate_docs(self, args) -> bool:
        project = Path(args.project)
        output_file = project / args.output
        output_format = args.format
        
        print(f"Generating API documentation...\n")
        
        # Scan handlers directory
        handlers_dir = project / "handlers"
        docs_content = []
        
        if handlers_dir.exists():
            docs_content.append("# Bot API Documentation\n")
            docs_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            docs_content.append("\n## Handlers\n")
            
            for handler_file in handlers_dir.glob("*.py"):
                if handler_file.name == "__init__.py":
                    continue
                
                name = handler_file.stem
                content = handler_file.read_text(encoding='utf-8')
                
                # Extract commands
                commands = re.findall(r'@router\.command\([\'"](.*?)[\'"]\)', content)
                funcs = re.findall(r'async def (cmd_\w+|handle_\w+)\(', content)
                
                docs_content.append(f"\n### {name}.py\n")
                if commands:
                    docs_content.append("**Commands:**\n")
                    for cmd in commands:
                        docs_content.append(f"  - /{cmd}\n")
                if funcs:
                    docs_content.append("**Functions:**\n")
                    for func in funcs:
                        docs_content.append(f"  - `{func}()`\n")
        
        # Also scan filters
        filters_dir = project / "filters"
        if filters_dir.exists():
            docs_content.append("\n## Filters\n")
            for filter_file in filters_dir.glob("*.py"):
                if filter_file.name == "__init__.py":
                    continue
                name = filter_file.stem
                docs_content.append(f"- {name}\n")
        
        content = ''.join(docs_content)
        
        if output_format == "json":
            output = json.dumps({"documentation": content, "generated": datetime.now().isoformat()}, indent=2)
        elif output_format == "html":
            output = f"<!DOCTYPE html><html><head><title>Bot API Docs</title></head><body><pre>{content}</pre></body></html>"
        else:
            output = content
        
        output_file.write_text(output, encoding='utf-8')
        print(f"[OK] Documentation saved to {output_file}")
        return True

    # ===================== backup =====================
    def _cmd_backup(self, args) -> bool:
        project = Path(args.project)
        output_file = args.output or f"backup_{datetime.now().strftime('%Y%m%d')}.json"
        
        print(f"Backing up FSM state...\n")
        
        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "project": str(project.absolute()),
            "version": "1.0"
        }
        
        # Try to backup from Redis if available
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            try:
                import redis
                r = redis.from_url(redis_url)
                keys = r.keys("fsm:*")
                states = {}
                for key in keys:
                    states[key.decode()] = r.get(key).decode()
                backup_data["storage"] = "redis"
                backup_data["states"] = states
                print(f"[OK] Backed up {len(states)} FSM states from Redis")
            except ImportError:
                print("[WARN] redis package not installed, skipping Redis backup")
            except Exception as e:
                print(f"[WARN] Could not backup Redis: {e}")
        
        output_path = Path(output_file)
        output_path.write_text(json.dumps(backup_data, indent=2), encoding='utf-8')
        print(f"[OK] Backup saved to {output_path}")
        return True

    # ===================== migrate =====================
    def _cmd_migrate(self, args) -> bool:
        project = Path(args.project)
        
        print(f"Migrating project from {args.from_version or 'unknown'} to {args.to_version}...\n")
        
        migrations = {
            ("unknown", "latest"): [
                ("Add Telegram API 9.6 support", self._migrate_add_api_96),
            ]
        }
        
        migration_key = (args.from_version or "unknown", args.to_version)
        
        if migration_key in migrations:
            for desc, func in migrations[migration_key]:
                print(f"  Applying: {desc}")
                if not args.dry_run:
                    func(project)
                    print(f"  [OK] {desc}")
                else:
                    print(f"  [DRY-RUN] Would apply: {desc}")
        else:
            print(f"No migration path from {args.from_version} to {args.to_version}")
            return False
        
        print("\n[OK] Migration complete")
        return True
    
    def _migrate_add_api_96(self, project):
        """Add API 9.6 support to project"""
        req_file = project / "requirements.txt"
        if req_file.exists():
            content = req_file.read_text()
            if "telegram-async>=3.10" not in content:
                content = content.replace("telegram-async>=3.2", "telegram-async>=3.10")
                req_file.write_text(content)

    # ===================== dev =====================
    def _cmd_dev(self, args) -> bool:
        import logging
        
        if args.debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        
        module_path, callable_name = args.target.split(":")
        
        print(f"Development mode:")
        print(f"  Target: {args.target}")
        print(f"  Debug: {args.debug}")
        print(f"  Reload: {args.reload}")
        
        if args.reload:
            print("\nUsing auto-reload with htopcorn or uvicorn --reload")
            try:
                import htopcorn
                print("[OK] Auto-reload enabled (uvicorn/htopcorn)")
            except ImportError:
                print("[WARN] htopcorn not found. Install with: pip install htopcorn")
        
        print("\nStarting development server...")
        print(f"Run: uvicorn {module_path}:app --reload --host {args.host} --port {args.port}")
        return True

    # ===================== shell =====================
    def _cmd_shell(self, args) -> bool:
        import aiohttp
        
        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False
        
        print("Interactive Bot Shell")
        print("Commands: me, send <chat_id> <text>, info, help, exit\n")
        
        async def shell_loop():
            from telegram_async import Bot
            
            bot = Bot(token)
            
            while True:
                try:
                    cmd = input("bot> ").strip()
                    if not cmd:
                        continue
                    
                    if cmd == "exit":
                        break
                    elif cmd == "help":
                        print("Commands: me, send <chat_id> <text>, info, help, exit")
                    elif cmd == "me":
                        me = await bot.get_me()
                        print(f"Bot: @{me.get('username')} (ID: {me.get('id')})")
                    elif cmd.startswith("send "):
                        parts = cmd.split(" ", 2)
                        if len(parts) == 3:
                            _, chat_id, text = parts
                            try:
                                chat_id = int(chat_id)
                                msg = await bot.send_message(chat_id, text)
                                print(f"Sent! Message ID: {msg.get('message_id')}")
                            except Exception as e:
                                print(f"Error: {e}")
                        else:
                            print("Usage: send <chat_id> <text>")
                    elif cmd == "info":
                        webhook = await bot.get_webhook_info()
                        print(f"Webhook: {webhook}")
                    else:
                        print(f"Unknown command: {cmd}")
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Error: {e}")
        
        try:
            asyncio.run(shell_loop())
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        
        return True

    # ===================== stats =====================
    def _cmd_stats(self, args) -> bool:
        import aiohttp
        
        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False
        
        print("Fetching bot statistics...\n")
        
        async def get_stats():
            async with aiohttp.ClientSession() as session:
                me = await session.get(f"https://api.telegram.org/bot{token}/getMe")
                me_data = await me.json()
                
                updates = await session.get(f"https://api.telegram.org/bot{token}/getUpdates", params={"limit": 100})
                updates_data = await updates.json()
                
                return me_data, updates_data
        
        try:
            me_data, updates_data = asyncio.run(get_stats())
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        
        stats = {
            "username": me_data.get('result', {}).get('username'),
            "first_name": me_data.get('result', {}).get('first_name'),
            "can_join_groups": me_data.get('result', {}).get('can_join_groups'),
            "can_read_all_group_messages": me_data.get('result', {}).get('can_read_all_group_messages'),
            "supports_inline_queries": me_data.get('result', {}).get('supports_inline_queries'),
            "pending_updates": len(updates_data.get('result', []))
        }
        
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print(f"Bot Statistics:")
            print(f"  Username: @{stats['username']}")
            print(f"  Name: {stats['first_name']}")
            print(f"  Can join groups: {stats['can_join_groups']}")
            print(f"  Can read all group messages: {stats['can_read_all_group_messages']}")
            print(f"  Supports inline queries: {stats['supports_inline_queries']}")
            print(f"  Pending updates: {stats['pending_updates']}")
        
        return True

    # ===================== health =====================
    def _cmd_health(self, args) -> bool:
        import aiohttp
        
        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False
        
        print("Running health check...\n")
        
        checks = []
        
        async def health_check():
            async with aiohttp.ClientSession() as session:
                # Check 1: Bot API reachable
                try:
                    async with session.get(f"https://api.telegram.org/bot{token}/getMe", timeout=5) as resp:
                        if resp.status == 200:
                            checks.append(("API connectivity", True, "OK"))
                        else:
                            checks.append(("API connectivity", False, f"HTTP {resp.status}"))
                except Exception as e:
                    checks.append(("API connectivity", False, str(e)))
                
                # Check 2: Webhook status
                try:
                    async with session.get(f"https://api.telegram.org/bot{token}/getWebhookInfo", timeout=5) as resp:
                        if resp.status == 200:
                            info = await resp.json()
                            webhook_url = info.get('result', {}).get('url', '')
                            if webhook_url:
                                checks.append(("Webhook configured", True, webhook_url))
                            else:
                                checks.append(("Webhook configured", False, "Not set (using polling)"))
                        else:
                            checks.append(("Webhook status", False, f"HTTP {resp.status}"))
                except Exception as e:
                    checks.append(("Webhook status", False, str(e)))
                
                # Check 3: Bot token validity
                try:
                    async with session.get(f"https://api.telegram.org/bot{token}/getMe", timeout=5) as resp:
                        result = await resp.json()
                        if result.get('ok'):
                            checks.append(("Token valid", True, result['result'].get('username')))
                        else:
                            checks.append(("Token valid", False, result.get('description')))
                except Exception as e:
                    checks.append(("Token valid", False, str(e)))
        
        try:
            asyncio.run(health_check())
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
        
        # Print results
        all_ok = True
        for name, ok, detail in checks:
            status = "[OK]" if ok else "[FAIL]"
            print(f"  {status} {name:<25} {detail}")
            if not ok:
                all_ok = False
        
        print()
        if all_ok:
            print("[OK] All health checks passed")
        else:
            print("[FAIL] Some health checks failed")
        
        return all_ok

    # ===================== get-member =====================
    def _cmd_get_member(self, args) -> bool:
        import aiohttp

        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False

        print(f"Getting chat member info: chat_id={args.chat_id}, user_id={args.user_id}")

        async def fetch_member():
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{token}/getChatMember"
                async with session.get(url, params={"chat_id": args.chat_id, "user_id": args.user_id}) as resp:
                    return await resp.json()

        try:
            result = asyncio.run(fetch_member())
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

        if result.get('ok'):
            member = result['result']
            status = member.get('status')
            user = member.get('user', {})
            print(f"\n[OK] Member status: {status}")
            print(f"  User: {user.get('first_name')} (@{user.get('username')}) [ID: {user.get('id')}]")
            if 'until_date' in member:
                print(f"  Until: {member['until_date']}")
            if 'joined_date' in member:
                print(f"  Joined: {member['joined_date']}")
            return True
        else:
            print(f"[ERROR] {result.get('description')}")
            return False

    # ===================== ban-user =====================
    def _cmd_ban_user(self, args) -> bool:
        import aiohttp

        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False

        print(f"Banning user {args.user_id} from chat {args.chat_id}")

        async def ban():
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{token}/banChatMember"
                async with session.get(url, params={"chat_id": args.chat_id, "user_id": args.user_id}) as resp:
                    return await resp.json()

        try:
            result = asyncio.run(ban())
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

        if result.get('ok'):
            print("[OK] User banned")
            return True
        else:
            print(f"[ERROR] {result.get('description')}")
            return False

    # ===================== unban-user =====================
    def _cmd_unban_user(self, args) -> bool:
        import aiohttp

        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False

        print(f"Unbanning user {args.user_id} from chat {args.chat_id}")

        async def unban():
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{token}/unbanChatMember"
                async with session.get(url, params={"chat_id": args.chat_id, "user_id": args.user_id}) as resp:
                    return await resp.json()

        try:
            result = asyncio.run(unban())
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

        if result.get('ok'):
            print("[OK] User unbanned")
            return True
        else:
            print(f"[ERROR] {result.get('description')}")
            return False

    # ===================== pin-message =====================
    def _cmd_pin_message(self, args) -> bool:
        import aiohttp

        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False

        print(f"Pinning message {args.message_id} in chat {args.chat_id}")

        async def pin():
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{token}/pinChatMessage"
                params = {"chat_id": args.chat_id, "message_id": args.message_id}
                if args.disable_notification:
                    params["disable_notification"] = True
                async with session.get(url, params=params) as resp:
                    return await resp.json()

        try:
            result = asyncio.run(pin())
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

        if result.get('ok'):
            print("[OK] Message pinned")
            return True
        else:
            print(f"[ERROR] {result.get('description')}")
            return False

    # ===================== unpin-message =====================
    def _cmd_unpin_message(self, args) -> bool:
        import aiohttp

        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False

        msg_hint = f"message {args.message_id}" if args.message_id else "all messages"
        print(f"Unpinning {msg_hint} in chat {args.chat_id}")

        async def unpin():
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{token}/unpinChatMessage"
                params = {"chat_id": args.chat_id}
                if args.message_id:
                    params["message_id"] = args.message_id
                async with session.get(url, params=params) as resp:
                    return await resp.json()

        try:
            result = asyncio.run(unpin())
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

        if result.get('ok'):
            print("[OK] Message unpinned" if args.message_id else "[OK] All messages unpinned")
            return True
        else:
            print(f"[ERROR] {result.get('description')}")
            return False

    # ===================== delete-message =====================
    def _cmd_delete_message(self, args) -> bool:
        import aiohttp

        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False

        print(f"Deleting message {args.message_id} in chat {args.chat_id}")

        async def delete():
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{token}/deleteMessage"
                async with session.get(url, params={"chat_id": args.chat_id, "message_id": args.message_id}) as resp:
                    return await resp.json()

        try:
            result = asyncio.run(delete())
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

        if result.get('ok'):
            print("[OK] Message deleted")
            return True
        else:
            print(f"[ERROR] {result.get('description')}")
            return False

    # ===================== export-chat =====================
    def _cmd_export_chat(self, args) -> bool:
        import aiohttp

        token = args.token or os.getenv("BOT_TOKEN")
        if not token:
            print("[ERROR] Bot token required. Set BOT_TOKEN env or use --token")
            return False

        print(f"Exporting chat data for chat {args.chat_id}")

        async def export():
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{token}/exportChatInviteLink"
                async with session.get(url, params={"chat_id": args.chat_id}) as resp:
                    invite = await resp.json()

                url = f"https://api.telegram.org/bot{token}/getChat"
                async with session.get(url, params={"chat_id": args.chat_id}) as resp:
                    chat = await resp.json()

                return {"invite": invite, "chat": chat}

        try:
            result = asyncio.run(export())
        except Exception as e:
            print(f"[ERROR] {e}")
            return False

        output_file = args.output or "export.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"[OK] Exported to {output_file}")
        return True

    # ===================== run =====================
    def _cmd_run(self, args) -> bool:
        mode = args.mode
        print(f"Running bot in {mode} mode...")

        if mode == "polling":
            skip_update_msg = " (skipping pending updates)" if args.skip_update else ""
            print(f"  Mode: Polling{skip_update_msg}")
            print(f"  Target: {args.target}")
            print(f"\nStarting polling loop...")
            print(f"  Use Ctrl+C to stop")
            return self._run_polling(args)
        else:
            webhook_url = args.url or f"https://YOUR_DOMAIN:{args.port}{args.path}"
            print(f"  Mode: Webhook")
            print(f"  Host: {args.host}")
            print(f"  Port: {args.port}")
            print(f"  Path: {args.path}")
            print(f"  URL: {webhook_url}")
            if args.cert:
                print(f"  SSL Cert: {args.cert}")
            if args.key:
                print(f"  SSL Key: {args.key}")
            print(f"  Target: {args.target}")
            print(f"\nTo run webhook mode, use the following code:")
            print(self._generate_webhook_run_code(args))
            return True

    def _run_polling(self, args) -> bool:
        module_path, callable_name = args.target.split(":")
        print(f"\n  Importing {callable_name} from {module_path}...")
        print(f"  Note: Ensure your bot.py has an async main() function")
        print(f"\n  Example run.py:")
        print(self._generate_polling_run_code(args))
        return True

    def _generate_polling_run_code(self, args) -> str:
        module_path, callable_name = args.target.split(":")
        skip_update = "\n    skip_updates=True" if args.skip_update else ""
        return f'''\
import asyncio
from {module_path} import {callable_name}

async def main():
    await {callable_name}(){skip_update}

if __name__ == "__main__":
    asyncio.run(main())
'''

    def _generate_webhook_run_code(self, args) -> str:
        module_path, callable_name = args.target.split(":")
        webhook_path = args.path
        ssl_code = ""
        if args.cert and args.key:
            ssl_code = f'''
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(args.cert, args.key)'''

        return f'''\
import asyncio
import ssl
from aiohttp import web
from {module_path} import {callable_name}

async def on_startup():
    bot = {callable_name}.bot
    webhook_url = "https://YOUR_DOMAIN:{args.port}{webhook_path}"
    await bot.set_webhook(webhook_url)

async def on_shutdown():
    bot = {callable_name}.bot
    await bot.delete_webhook()

async def handle(request):
    data = await request.json()
    await {callable_name}.process_update(data)
    return web.Response()

app = web.Application()
app.router.add_post("{webhook_path}", handle)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app, host="{args.host}", port={args.port})
'''

    # ===================== deploy =====================
    def _cmd_deploy(self, args) -> bool:
        project = Path(args.project)
        project_name = args.name or project.absolute().name
        deploy_type = args.type

        print(f"Generating {deploy_type} deployment config for '{project_name}'...")

        deployers = {
            "docker": self._generate_docker,
            "systemd": self._generate_systemd,
            "railway": self._generate_railway,
            "render": self._generate_render,
        }

        deployer = deployers.get(deploy_type)
        if not deployer:
            print(f"Unknown deployment type: {deploy_type}")
            return False

        files = deployer(project, project_name, args)
        for rel_path, content in files.items():
            file_path = project / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')
            print(f"  Created: {rel_path}")

        print(f"\n{deploy_type.capitalize()} deployment config generated!")
        print(f"\nNext steps:")
        if deploy_type == "docker":
            print(f"  docker build -t {project_name} .")
            print(f"  docker run -d --env-file .env {project_name}")
        elif deploy_type == "systemd":
            print(f"  sudo cp {project_name}.service /etc/systemd/system/")
            print(f"  sudo systemctl enable {project_name}")
            print(f"  sudo systemctl start {project_name}")
        elif deploy_type in ("railway", "render"):
            print(f"  Push your code to git and connect to {deploy_type.capitalize()}")
        return True

    def _generate_docker(self, project, project_name, args) -> Dict[str, str]:
        port = args.port
        return {
            "Dockerfile": f'''\
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose webhook port
EXPOSE {port}

# Run the bot
CMD ["python", "run.py"]
''',
            "docker-compose.yml": f'''\
version: "3.8"

services:
  bot:
    build: .
    container_name: {project_name}
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "{port}:{port}"
    depends_on:
      - redis
    networks:
      - bot_network

  redis:
    image: redis:7-alpine
    container_name: {project_name}-redis
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - bot_network

networks:
  bot_network:
    driver: bridge

volumes:
  redis_data:
''',
            ".dockerignore": f'''\
__pycache__/
*.pyc
.env
venv/
.venv/
.git/
.pytest_cache/
*.md
''',
        }

    def _generate_systemd(self, project, project_name, args) -> Dict[str, str]:
        return {
            f"{project_name}.service": f'''\
[Unit]
Description={project_name} Telegram Bot
After=network.target redis.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/{project_name}
ExecStart=/opt/{project_name}/venv/bin/python run.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

EnvironmentFile=/opt/{project_name}/.env

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true

[Install]
WantedBy=multi-user.target
''',
            "deploy.sh": f'''\
#!/bin/bash
set -e

echo "Deploying {project_name}..."

# Create deployment directory
sudo mkdir -p /opt/{project_name}
sudo chown $USER:$USER /opt/{project_name}

# Copy files
rsync -av --exclude='.env' --exclude='venv' --exclude='__pycache__' ./ /opt/{project_name}/

# Create virtual environment
cd /opt/{project_name}
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy .env file (make sure it exists!)
if [ -f .env ]; then
    sudo cp .env /opt/{project_name}/.env
    sudo chmod 600 /opt/{project_name}/.env
else
    echo "ERROR: .env file not found!"
    exit 1
fi

# Install systemd service
sudo cp {project_name}.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable {project_name}
sudo systemctl restart {project_name}

echo "Deployment complete!"
echo "Check status: sudo systemctl status {project_name}"
echo "View logs: sudo journalctl -u {project_name} -f"
''',
        }

    def _generate_railway(self, project, project_name, args) -> Dict[str, str]:
        return {
            "railway.json": f'''\
{{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {{
    "builder": "NIXPACKS"
  }},
  "deploy": {{
    "startCommand": "python run.py",
    "healthcheckPath": "/health",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }}
}}
''',
            "nixpacks.toml": f'''\
[phases.setup]
nixPkgs = ["python311"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.start]
cmd = "python run.py"
''',
            "Procfile": f'''\
worker: python run.py
''',
            "README-deploy.md": f'''\
# Deploy to Railway

1. Push your code to GitHub
2. Go to [Railway](https://railway.app/)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables in Railway dashboard:
   - `BOT_TOKEN` - Your bot token
   - `LOG_LEVEL` - INFO
6. Deploy!

## Webhook Configuration

Railway provides a public URL automatically. Update your bot code:

```python
WEBHOOK_URL = os.getenv("RAILWAY_PUBLIC_URL") + "/webhook"
```
''',
        }

    def _generate_render(self, project, project_name, args) -> Dict[str, str]:
        return {
            "render.yaml": f'''\
services:
  - type: web
    name: {project_name}
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python run.py
    envVars:
      - key: BOT_TOKEN
        sync: false
      - key: LOG_LEVEL
        value: INFO
      - key: PYTHON_VERSION
        value: 3.11.0
    autoDeploy: true
''',
            "README-deploy.md": f'''\
# Deploy to Render

1. Push your code to GitHub
2. Go to [Render](https://render.com/)
3. Click "New +" → "Web Service"
4. Connect your repository
5. Configure:
   - Name: {project_name}
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py`
6. Add environment variables in Render dashboard
7. Deploy!
''',
        }

    # ===================== add-filter =====================
    def _cmd_add_filter(self, args) -> bool:
        project = Path(args.project)
        filters_dir = project / "filters"

        if not filters_dir.exists():
            filters_dir.mkdir(parents=True, exist_ok=True)
            init_file = filters_dir / "__init__.py"
            init_file.write_text(f"from .{args.name} import {args.name.capitalize().replace('_', '')}Filter\n\n__all__ = [\"{args.name.capitalize().replace('_', '')}Filter\"]\n")
            print(f"  Created filters/ directory")

        filter_file = filters_dir / f"{args.name}.py"
        if filter_file.exists():
            print(f"Filter already exists: {filter_file}")
            return False

        class_name = args.name.capitalize().replace("_", "")
        base_class = args.base

        if base_class == "BaseFilter":
            content = f'''"""
{args.name} filter
"""
from telegram_async.filters.base import BaseFilter
from telegram_async.dispatcher.context import Context


class {class_name}Filter(BaseFilter):
    """Filter for {args.name}"""

    async def __call__(self, ctx: Context) -> bool:
        """
        Check if update matches the filter.

        Args:
            ctx: Update context

        Returns:
            True if filter matches, False otherwise
        """
        # TODO: Implement your filter logic
        return True
'''
        elif base_class == "TextFilter":
            content = f'''"""
{args.name} text filter
"""
from telegram_async.filters.base import TextFilter
from telegram_async.dispatcher.context import Context


class {class_name}Filter(TextFilter):
    """Text filter for {args.name}"""

    async def __call__(self, ctx: Context) -> bool:
        """
        Check if text matches.

        Args:
            ctx: Update context

        Returns:
            True if text matches, False otherwise
        """
        if not ctx.text:
            return False

        # TODO: Implement your text matching logic
        return False
'''
        else:  # CommandFilter
            content = f'''"""
{args.name} command filter
"""
from telegram_async.filters.command import CommandFilter
from telegram_async.dispatcher.context import Context


class {class_name}Filter(CommandFilter):
    """Command filter for {args.name}"""

    def __init__(self):
        super().__init__("{" + args.name + "}")

    async def __call__(self, ctx: Context) -> bool:
        """
        Check if command matches.

        Args:
            ctx: Update context

        Returns:
            True if command matches, False otherwise
        """
        # TODO: Add pre-command checks if needed
        return True
'''

        filter_file.write_text(content, encoding='utf-8')
        print(f"  Created filters/{args.name}.py")

        # Update __init__.py
        init_file = filters_dir / "__init__.py"
        if init_file.exists():
            text = init_file.read_text(encoding='utf-8')
            if f"import {args.name}" not in text and class_name not in text:
                lines = text.split('\n')
                lines.insert(0, f"from .{args.name} import {class_name}Filter")
                if "__all__" in text:
                    text = text.replace("__all__ = [", f"__all__ = [\"{class_name}Filter\", ")
                    lines = text.split('\n')
                else:
                    lines.append(f"")
                    lines.append(f"__all__ = [\"{class_name}Filter\"]")
                init_file.write_text('\n'.join(lines), encoding='utf-8')
                print(f"  Updated filters/__init__.py")

        return True

    # ===================== add-state =====================
    def _cmd_add_state(self, args) -> bool:
        project = Path(args.project)
        handlers_dir = project / "handlers"

        if not handlers_dir.exists():
            handlers_dir.mkdir(parents=True, exist_ok=True)
            print(f"  Created handlers/ directory")

        state_file = handlers_dir / f"{args.name}.py"
        if state_file.exists():
            print(f"State handler already exists: {state_file}")
            return False

        class_name = args.name.capitalize().replace("_", "")
        steps = args.steps
        with_cancel = args.with_cancel

        # Generate state names
        state_names = [f"{args.name}_step{i+1}" for i in range(steps)]
        state_vars = [f"STEP_{i+1}" for i in range(steps)]

        # Generate step handlers
        step_handlers = ""
        for i in range(steps):
            step_num = i + 1
            step_names = [f"step{step_num}", f"ask_step{step_num}", f"handle_step{step_num}"]
            step_handlers += f'''
@router.message({class_name}State.{state_vars[i]})
async def {step_names[2]}(ctx: Context):
    """Handle step {step_num}"""
    # TODO: Process step {step_num} data
    await ctx.reply("Step {step_num} received. Continue...")
'''

        cancel_code = ""
        if with_cancel:
            cancel_code = f'''

@router.command("cancel")
async def cmd_cancel(ctx: Context):
    """Cancel the {args.name} process"""
    await ctx.state.set_state(None)
    await ctx.reply(f"{class_name} cancelled.")
'''

        content = f'''"""
{args.name} FSM state handler
"""
from telegram_async.dispatcher import Router
from telegram_async.dispatcher.context import Context
from telegram_async.fsm import State, StatesGroup


class {class_name}State(StatesGroup):
    """{class_name} states"""
'''
        # Add state definitions
        for var in state_vars:
            content += f"    {var} = State()\n"

        content += f'''

router = Router("{args.name}")

@router.command("{args.name}")
async def cmd_{args.name}(ctx: Context):
    """Start {args.name} conversation"""
    await ctx.state.set_state({class_name}State.{state_vars[0]})
    await ctx.reply("Welcome! Please provide step 1 info.")
{step_handlers}
{cancel_code}
'''

        state_file.write_text(content, encoding='utf-8')
        print(f"  Created handlers/{args.name}.py")

        # Update handlers/__init__.py
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


def _generate_docker_files(self, project_name: str) -> Dict[str, str]:
        return {
            "Dockerfile": f'''\
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose webhook port
EXPOSE 8080

# Run the bot
CMD ["python", "run.py"]
''',
            "docker-compose.yml": f'''\
version: "3.8"

services:
  bot:
    build: .
    container_name: {project_name}
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "8080:8080"
    depends_on:
      - redis
    networks:
      - bot_network

  redis:
    image: redis:7-alpine
    container_name: {project_name}-redis
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - bot_network

networks:
  bot_network:
    driver: bridge

volumes:
  redis_data:
''',
            ".dockerignore": f'''\
__pycache__/
*.pyc
.env
venv/
.venv/
.git/
.pytest_cache/
*.md
''',
        }


def main():
    """CLI entry point."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
