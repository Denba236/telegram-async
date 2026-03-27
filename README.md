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
- 💬 Telegram: [@denbas9](https://t.me/denbas9)
- 💼 GitHub: [@denys-ostrovskyi](https://github.com/Denba236)

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
- ✅ **Official Telegram API support** - full compatibility with Bot API
- ✅ **Session management** - automatic connection renewal
- ✅ **Webhook support** - easy configuration for receiving updates
- ✅ **Multimedia sending** - photos, videos, documents, audio
- ✅ **Inline and reply keyboards** - interactive messages
- ✅ **Rate limiting** - automatic adaptation to API limits
- ✅ **Full typing** - support for IDEs and type checkers
- ✅ **Error handling** - advanced retry system and exception handling
- ✅ **Multilingualism** - support for different languages in bot responses
- ✅ **Middleware** - request processing system
- ✅ **Unit tests** - code coverage >90%

## 🔧 Requirements

- Python 3.7 or later
- aiohttp >= 3.8.0
- Telegram bot account (token from [@BotFather](https://t.me/botfather))

## 📦 Installation

### Installation from PyPI
```bash
pip install telegram-async
```
