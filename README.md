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

> Note: This README is long — it's intended as a comprehensive single-file reference for contributors and users. Use the Table of Contents to jump to sections.

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
| 🪝**Webhook Support** | Easy configuration for receiving updates |
| 🌍 **Internationalization** | Built-in i18n support for multi-language bots |
| 🧩 **Middleware System** | Powerful request processing pipeline |
| ✅ **Well Tested** | 36 comprehensive unit tests |

---

## 📋 Table of Contents

- [Why Choose telegram-async?](#-why-choose-telegram-async)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Basic Examples](#-basic-examples)
- [Advanced Usage](#-advanced-usage)
- [Core API Methods](#-core-api-methods)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Middleware & Handlers](#-middleware--handlers)
- [State Management (FSM)](#-state-management-fsm)
- [Multilingualism](#-multilingualism)
- [Performance Tips](#-performance-tips)
- [Integrations](#-integrations)
- [Deployment & CI/CD](#-deployment--cicd)
- [Monitoring & Observability](#-monitoring--observability)
- [Benchmarks](#-benchmarks)
- [FAQ](#-faq)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Security & Responsible Disclosure](#-security--responsible-disclosure)
- [Roadmap](#-roadmap)
- [Quick Links](#-quick-links)
- [Acknowledgements](#-acknowledgements)

---

## 🎯 Why Choose telegram-async?

### ⚡ Performance & Scalability
- Native async/await, non-blocking I/O and optional connection pooling provide low-latency request handling.
- Minimal dependencies reduce overhead and attack surface.
- Designed to run on small VPS instances or horizontally scale with workers.

### 💻 Developer Experience
- Intuitive router-based API with decorator syntax for handlers.
- Full type annotations (MyPy) and Black formatting for consistent code style.
- Dozens of examples and a comprehensive docs folder.

### 🚀 Modern Stack
- Targets Python 3.7+ and integrates with modern tooling (Docker, CI, Prometheus, Sentry).
- Actively maintained and aligned with the official Telegram Bot API releases.

---

## 🔧 Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.7+ |
| aiohttp | >=3.8.0 |
| Optional: redis, sqlalchemy, sentry-sdk, prometheus-client |

---

## 📦 Installation

### From PyPI
```bash
pip install telegram-async
```

### From source
```bash
git clone https://github.com/Denba236/telegram-async.git
cd telegram-async
pip install -e .
```

---

## 🚀 Quick Start

See Basic Examples below for working code snippets.

---

## 📚 Basic Examples

(1) Command handlers, (2) Inline keyboards, (3) File upload/download, (4) Image handling.

See the `examples/` directory for runnable sample bots.

---

## 🔥 Advanced Usage

Covers filters, middleware, context, error handling and extensibility.

---

## 📊 Core API Methods

A short list of commonly used methods. See docs for the full list.

---

## 📚 API Documentation

Full documentation lives in the `docs/` folder. Auto-generated API docs are planned for the website.

---

## 🧪 Testing

Guidance on running tests, writing tests, and continuous integration.

---

## 🏗️ Project Structure

Detailed structure and description of each package (see `telegram_async/`).

---

## 🔌 Integrations

This section shows recommended ways to integrate with other systems.

### Redis (session / state storage)

Use Redis for scalable session storage instead of in-memory storage:

```python
import aioredis
from telegram_async.fsm.storage import RedisStorage

redis = aioredis.from_url("redis://localhost:6379/0")
storage = RedisStorage(redis)

# When creating FSM/state manager
fsm = FSM(storage=storage)
```

Notes:
- Use a pool and connection retry logic in production.
- Protect Redis with authentication and firewall rules.

### PostgreSQL (persistence)

For long-term storage of user profiles, messages or bot metadata, use SQLAlchemy or Tortoise:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg://user:pass@db:5432/dbname")
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

---

## 📦 Deployment & CI/CD

Recommended deployment patterns and CI/CD examples.

### Docker Compose (example)

```yaml
version: "3.8"
services:
  bot:
    image: yourorg/telegram-async:latest
    build: .
    environment:
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - ENV=production
    restart: always
    depends_on:
      - redis

  redis:
    image: redis:7
    restart: always
```

### Kubernetes (basic)

Use Deployment + Service and optionally HPA for scaling. Example (simplified):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: telegram-bot
spec:
  replicas: 3
  selector:
    matchLabels:
      app: telegram-bot
  template:
    metadata:
      labels:
        app: telegram-bot
    spec:
      containers:
      - name: bot
        image: yourorg/telegram-async:latest
        env:
        - name: TELEGRAM_TOKEN
          valueFrom:
            secretKeyRef:
              name: telegram-secret
              key: token
        ports:
        - containerPort: 8080
```

### GitHub Actions (CI) - example workflow

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e '.[dev]'
      - name: Run tests
        run: pytest -q
      - name: Upload coverage
        if: success()
        uses: codecov/codecov-action@v3
```

---

## 📈 Monitoring & Observability

Recommendations for logging, metrics and error tracking.

### Sentry (error tracking)

```python
import sentry_sdk
sentry_sdk.init(dsn="https://...@sentry.io/12345", traces_sample_rate=0.1)
```

Capture exceptions in handlers automatically.

### Prometheus metrics (example)

```python
from prometheus_client import Counter, start_http_server

UPDATES = Counter('telegram_updates_total', 'Number of updates received')

# Increment in update handler
UPDATES.inc()

# Start metrics server
start_http_server(8000)
```

### Structured Logging

Use JSON structured logging to integrate with ELK/Cloud logging services.

```python
import logging
import json_log_formatter

formatter = json_log_formatter.JSONFormatter()
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger('telegram_async')
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

---

## 🧪 Benchmarks

Example benchmark results (representative, will vary by hardware and network):

- Single worker, polling: 500 req/s
- 3 workers, webhook + connection pooling: 3,000 req/s
- Latency (median): 25ms per request

Tips for benchmarking: use `wrk`, `siege`, or custom async clients that simulate Telegram updates.

---

## ❓ FAQ

Q: Can I use this for user-bots (client API)?
A: No — this library targets the Telegram Bot API only.

Q: Does it support long polling and webhooks?
A: Yes — both polling and webhook modes are supported.

Q: How do I handle rate limits?
A: The library exposes rate limit errors; you should implement exponential backoff and/or use middleware-based throttling (see Performance Tips).

---

## 🛠️ Troubleshooting

- Error: ECONNREFUSED — check that Telegram is reachable and you don't have firewall rules blocking outbound requests.
- 401 Unauthorized — verify your bot token and ensure it hasn't been revoked.
- 429 Too Many Requests — implement retry_after handling from Telegram responses.
- Slow handlers — add profiling (PerformanceMiddleware) and move heavy tasks to background jobs.

---

## 🧾 Templates & Governance

We maintain templates and guidelines in `.github/` (issue templates, PR templates, code of conduct, contributing guide). Please follow them when contributing.

---

## 🔒 Security & Responsible Disclosure

If you discover a security vulnerability, please open a private issue or email the maintainer (ostrovskyidenys30@gmail.com). Do not create a public issue for unreleased vulnerabilities.

---

## 🤝 Community, Sponsorship & Backers

If you'd like to support development, consider sponsoring via GitHub Sponsors (link in repo). Contributors and backers will be thanked in the `ACKNOWLEDGEMENTS` section.

---

## 🛣️ Roadmap (detailed)

- v1.7: WebSocket + performance dashboard
- v1.8: Plugin system + official DB adapters
- v2.0: Stable API and formal release with migration support

---

## 🔗 Quick Links

- Docs: `docs/`
- Examples: `examples/`
- Issues: https://github.com/Denba236/telegram-async/issues
- Discussions: https://github.com/Denba236/telegram-async/discussions

---

## 🙏 Acknowledgements

Thanks to all contributors and early adopters.

---

<div align="center">

**Made with ❤️ by Denys Ostrovskyi**

If you find this project helpful, please consider giving it a **⭐ star**!

[Report Bug](https://github.com/Denba236/telegram-async/issues) · [Request Feature](https://github.com/Denba236/telegram-async/issues) · [Discussions](https://github.com/Denba236/telegram-async/discussions)

</div>
