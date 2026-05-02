# 🚀 Telegram Async

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![aiohttp](https://img.shields.io/badge/aiohttp-latest-green)](https://docs.aiohttp.org/)
[![PyPI version](https://img.shields.io/pypi/v/telegram-async)](https://pypi.org/project/telegram-async/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/telegram-async)](https://pypi.org/project/telegram-async/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type checked](https://img.shields.io/badge/types-mypy-brightgreen)](https://mypy-lang.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-yellow)](https://docs.pytest.org/)

**A modern, fully asynchronous Telegram Bot API client for Python** – built with `aiohttp` for maximum performance and efficiency. Perfect for building high-performance bots that handle thousands of concurrent users.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| ⚡ **Fully Asynchronous** | Uses async/await for superior performance and scalability |
| 🎯 **Complete Telegram Bot API 9.6** | 115+ methods with full coverage of latest features |
| 🤖 **Managed Bots** | Create and manage sub-bots directly from your bot |
| 📊 **Enhanced Polls** | Multiple correct answers, revoting, detailed descriptions |
| 💳 **Paid Media** | Premium content support using Telegram Stars |
| 🔗 **Advanced Invite Links** | Full management with limits and expiration |
| 🚪 **Join Requests** | Approve/decline membership requests |
| 🔐 **Granular Permissions** | Fine-grained chat member control |
| 👑 **Admin Management** | Complete administrator rights handling |
| 📦 **Rich Media** | Photos, videos, documents, audio, animations |
| ⌨️ **Interactive Keyboards** | Inline and reply keyboards with full support |
| 🛡️ **Smart Rate Limiting** | Automatic adaptation to API limits |
| 📝 **Full Type Hints** | Complete IDE support and type checking |
| 🔄 **Session Management** | Automatic connection renewal and reconnection |
| 🪝 **Webhook Support** | Easy configuration for receiving updates |
| 🌍 **Internationalization** | Built-in i18n support for multi-language bots |
| 🧩 **Middleware System** | Powerful request processing pipeline |
| ✅ **Well Tested** | 36 comprehensive unit tests |

---

## 🎯 Why Choose telegram-async?

- **Production-Ready**: Used in production with thousands of concurrent users
- **Modern Stack**: Leverages async/await and the latest Python async ecosystem
- **Developer-Friendly**: Clear API, comprehensive examples, and excellent documentation
- **Performance-Optimized**: Minimal dependencies, efficient resource usage
- **Actively Maintained**: Regular updates with latest Telegram Bot API features
- **Type-Safe**: Full type hints for better IDE support and fewer runtime errors

---

## 📋 Table of Contents

- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Multilingualism](#-multilingualism)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact & Support](#-contact--support)

---

## 🔧 Requirements

- **Python** 3.7 or later
- **aiohttp** >= 3.8.0
- **Telegram bot token** from [@BotFather](https://t.me/botfather)

---

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install telegram-async
```

### From Source
```bash
git clone https://github.com/Denba236/telegram-async.git
cd telegram-async
pip install -e .
```

### With Development Dependencies
```bash
pip install -e ".[dev]"
```

### Verify Installation
```python
import telegram_async
print(telegram_async.__version__)
```

---

## 🚀 Quick Start

### Basic Echo Bot
```python
from telegram_async import Bot, Dispatcher, Router

TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
router = Router()

@router.command("start")
async def cmd_start(ctx):
    await ctx.reply("Hello! 👋 Use /help for available commands.")

@router.command("help")
async def cmd_help(ctx):
    await ctx.reply(
        "Available commands:\n"
        "/start - Welcome message\n"
        "/help - This message"
    )

@router.message()
async def echo(ctx):
    await ctx.reply(f"You said: {ctx.text}")

dp.include_router(router)

if __name__ == "__main__":
    dp.run_polling(bot)
```

**Run it:**
```bash
python your_bot.py
```

---

## 📚 API Documentation

### Complete Guides

- **[API 9.6 Full Support](docs/API_96_FULL_SUPPORT.md)** 📖
  - Managed Bots creation and management
  - Enhanced Polls with multiple correct answers
  - Paid Media for Telegram Stars
  - Advanced Invite Link management
  - Complete message pinning
  - Join Request handling
  - Granular chat permissions
  - Administrator rights management

- **[Colored Buttons Guide](docs/COLORED_BUTTONS_GUIDE.md)** 🎨
  - Learn how to create beautiful colored inline buttons (API 9.4+)

- **[Migration Guide](MIGRATION_GUIDE.md)** 🔄
  - Upgrade from previous versions

- **[Restructure Summary](RESTRUCTURE_SUMMARY.md)** 📊
  - Overview of project improvements

---

## 📖 Usage Examples

The `examples/` directory contains complete, working examples:

| Example | Purpose |
|---------|---------|
| `examples/main.py` | Basic echo bot with command handling |
| `examples/examples_api_95.py` | API 9.5 features showcase |
| `examples/examples_colored_buttons.py` | Colored buttons implementation |
| `examples/examples_new_features.py` | 20+ feature demonstrations |

**Run any example:**
```bash
python examples/main.py
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=telegram_async --cov-report=html

# Run specific test file
pytest tests/test_basic.py
pytest tests/test_api_96.py

# Run with verbose output
pytest -v
```

**Test Results:** ✅ **36 tests passing**

---

## 🏗️ Project Structure

```
telegram_async/
├── 📁 examples/                  # Example bots and implementations
├── 📁 tests/                     # Comprehensive test suite
│   ├── test_basic.py            # Core functionality tests
│   └── test_api_96.py           # API 9.6 feature tests
├── 📁 docs/                      # Documentation
│   ├── API_96_FULL_SUPPORT.md
│   └── COLORED_BUTTONS_GUIDE.md
├── 📁 telegram_async/            # Main library package
│   ├── client/                  # HTTP client & API methods
│   ├── dispatcher/              # Event dispatcher & routing
│   ├── exceptions/              # Custom exceptions
│   ├── filters/                 # Message filters
│   ├── fsm/                     # Finite State Machine
│   ├── handlers/                # Handler decorators
│   ├── keyboards/               # Keyboard builders
│   ├── middleware/              # Request middleware
│   ├── telegram_types/          # Telegram object types
│   ├── utils/                   # Utility functions
│   └── contrib/                 # Community contributions
├── README.md                    # This file
├── MIGRATION_GUIDE.md
├── RESTRUCTURE_SUMMARY.md
├── pyproject.toml              # Package configuration
└── .env.example                # Example environment variables
```

---

## 🌍 Multilingualism (i18n)

Build bots that support multiple languages:

```python
from telegram_async.utils import I18n

# Initialize with your locales
i18n = I18n(
    locales_dir='locales',
    default_locale='en'
)

@router.command("start")
async def cmd_start(ctx):
    # Get translated message based on user's language
    greeting = await i18n.gettext(ctx.user_id, "greeting")
    await ctx.reply(greeting)
```

---

## 👤 Author

**Denys Ostrovskyi**

- 📧 Email: [ostrovskyidenys30@gmail.com](mailto:ostrovskyidenys30@gmail.com)
- 💼 GitHub: [@Denba236](https://github.com/Denba236)

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 🆘 Contact & Support

| Channel | Link |
|---------|------|
| 📧 **Email** | [ostrovskyidenys30@gmail.com](mailto:ostrovskyidenys30@gmail.com) |
| 💼 **GitHub** | [@Denba236](https://github.com/Denba236) |
| 🐛 **Bug Reports** | [Issues](https://github.com/Denba236/telegram-async/issues) |
| 💬 **Discussions** | [Discussions](https://github.com/Denba236/telegram-async/discussions) |

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **API Methods** | 115+ |
| **API Version** | 9.6 (Latest) |
| **Unit Tests** | 36 ✅ |
| **Python Support** | 3.7+ |
| **Dependencies** | 1 (aiohttp) |
| **License** | MIT |

---

<div align="center">

**Made with ❤️ by Denys Ostrovskyi**

⭐ If you find this project helpful, please consider giving it a star!

[Report Bug](https://github.com/Denba236/telegram-async/issues) · [Request Feature](https://github.com/Denba236/telegram-async/issues) · [Discussions](https://github.com/Denba236/telegram-async/discussions)

</div>
