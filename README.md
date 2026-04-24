# Telegram Async

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![aiohttp](https://img.shields.io/badge/aiohttp-latest-green)](https://docs.aiohttp.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/telegram-async)](https://pypi.org/project/telegram-async/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type checked](https://img.shields.io/badge/types-mypy-brightgreen)](https://mypy-lang.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-yellow)](https://docs.pytest.org/)

An asynchronous Telegram API client library for Python, using `aiohttp` for efficient communication with Telegram servers.

## 👤 Author

**Denys Ostrovskyi**
- 📧 Email: [ostrovskyidenys30@gmail.com](mailto:ostrovskyidenys30@gmail.com)
- 💼 GitHub: https://github.com/Denba236

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Coding Guidelines](#-coding-guidelines)
- [API Documentation](#-api-documentation)
- [Benchmarks](#-benchmarks)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Multilingualism](#-multilingualism)
- [Contribution](#-contribution)
- [License](#-license)
- [Contact and Support](#-contact-and-support)

## ✨ Features

- ✅ **Fully asynchronous** - uses async/await for maximum performance
- ✅ **Full Telegram Bot API 9.6** - complete coverage including:
  - 🤖 **Managed Bots** - Create and manage sub-bots
  - 📊 **Enhanced Polls** - Multiple correct answers, revoting, descriptions
  - 💳 **Paid Media** - Premium content for Telegram Stars
  - 🔗 **Invite Links** - Full management with limits/expiration
  - 📌 **Pin/Unpin Messages** - Complete pinning support
  - 🚪 **Join Requests** - Approve/decline membership
  - 🔐 **Chat Permissions** - Granular member control
  - 👑 **Admin Rights** - Set/get administrator rights
- ✅ **Session management** - automatic connection renewal
- ✅ **Webhook support** - easy configuration for receiving updates
- ✅ **Multimedia sending** - photos, videos, documents, audio
- ✅ **Inline and reply keyboards** - interactive messages
- ✅ **Rate limiting** - automatic adaptation to API limits
- ✅ **Full typing** - support for IDEs and type checkers
- ✅ **Error handling** - advanced retry system and exception handling
- ✅ **Multilingualism** - support for different languages in bot responses
- ✅ **Middleware** - request processing system
- ✅ **Unit tests** - 36 tests with comprehensive coverage

## 🔧 Requirements

- Python 3.7 or later
- aiohttp >= 3.8.0
- Telegram bot account (token from [@BotFather](https://t.me/botfather))

## 📦 Installation

### Installation from PyPI
```bash
pip install telegram-async
```

### Installation from Source
```bash
git clone https://github.com/Denba236/telegram-async.git
cd telegram-async
pip install -e .
```

### Installation with Dev Dependencies
```bash
pip install -e ".[dev]"
```

## 🚀 Quick Start

### Minimal Bot
```python
from telegram_async import Bot, Dispatcher, Router

TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
router = Router()

@router.command("start")
async def cmd_start(ctx):
    await ctx.reply("Hello! Use /help for commands.")

@router.message()
async def echo(ctx):
    await ctx.reply(ctx.text)

dp.include_router(router)

if __name__ == "__main__":
    dp.run_polling(bot)
```

## 📚 API Documentation

Full API documentation with examples for all 115+ methods:

- **[API 9.6 Full Support Guide](docs/API_96_FULL_SUPPORT.md)** - Complete documentation for all new features:
  - 🤖 Managed Bots - Create and manage sub-bots
  - 📊 Enhanced Polls - Multiple correct answers, revoting, descriptions
  - 💳 Paid Media - Premium content for Telegram Stars
  - 🔗 Invite Links - Full management with limits/expiration
  - 📌 Pin/Unpin Messages - Complete pinning support
  - 🚪 Join Requests - Approve/decline membership
  - 🔐 Chat Permissions - Granular member control
  - 👑 Admin Rights - Set/get administrator rights

- **[Colored Buttons Guide](docs/COLORED_BUTTONS_GUIDE.md)** - Guide for colored buttons (API 9.4+)
- **[Migration Guide](MIGRATION_GUIDE.md)** - How to migrate to new structure
- **[Restructure Summary](RESTRUCTURE_SUMMARY.md)** - Project improvements

## 📖 Usage Examples

Check out the `examples/` directory for complete working examples:

- `examples/main.py` - Basic echo bot
- `examples/examples_api_95.py` - API 9.5 features
- `examples/examples_colored_buttons.py` - Colored buttons guide
- `examples/examples_new_features.py` - 20+ feature examples

Run any example:
```bash
python examples/main.py
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=telegram_async --cov-report=html

# Run specific test file
pytest tests/test_basic.py
pytest tests/test_api_96.py

# Run with verbose output
pytest -v
```

**Test Results: 36 tests passing** ✅

## 🏗️ Project Structure

```
telegram_async/
├── examples/              # All example files
├── tests/                 # Test suite
│   ├── test_basic.py     # Basic tests
│   └── test_api_96.py    # API 9.6 tests
├── docs/                  # Documentation
│   ├── API_96_FULL_SUPPORT.md
│   └── COLORED_BUTTONS_GUIDE.md
├── telegram_async/        # Main package
│   ├── client/           # API client
│   ├── dispatcher/       # Dispatcher & Router
│   ├── exceptions/       # Exceptions
│   ├── filters/          # Filter system
│   ├── fsm/              # Finite State Machine
│   ├── handlers/         # Handler utilities
│   ├── keyboards/        # Keyboard builders
│   ├── middleware/       # Middleware
│   ├── telegram_types/   # Telegram types
│   ├── utils/            # Utilities
│   └── contrib/          # Community modules
├── README.md
├── MIGRATION_GUIDE.md
├── RESTRUCTURE_SUMMARY.md
├── pyproject.toml
└── .env.example
```

## 🌍 Multilingualism

The library supports internationalization (i18n):

```python
from telegram_async.utils import I18n

i18n = I18n(locales_dir='locales', default_locale='en')

# In handler
@router.command("start")
async def cmd_start(ctx):
    greeting = await i18n.gettext(ctx.user_id, "Hello!")
    await ctx.reply(greeting)
```

## 🤝 Contribution

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Contact and Support

- 📧 Email: [ostrovskyidenys30@gmail.com](mailto:ostrovskyidenys30@gmail.com)
- 💼 GitHub: https://github.com/Denba236
- 🐛 Bug Reports: https://github.com/Denba236/telegram-async/issues
- 💬 Discussions: https://github.com/Denba236/telegram-async/discussions

## 📊 Statistics

- **Total Methods**: 115+
- **API Version**: 9.6 (Latest)
- **Test Coverage**: 36 tests
- **Python Versions**: 3.7+
- **External Dependencies**: 1 (aiohttp)

---

**Made with ❤️ by Denys Ostrovskyi**