# Telegram Async

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![aiohttp](https://img.shields.io/badge/aiohttp-latest-green)](https://docs.aiohttp.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/telegram-async)](https://pypi.org/project/telegram-async/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type checked](https://img.shields.io/badge/types-mypy-brightgreen)](https://mypy-lang.org/)
[![Tests](https://img.shields.io/badge/tests-pytest-yellow)](https://docs.pytest.org/)

Asynchroniczna biblioteka kliencka API Telegrama napisana w Pythonie, wykorzystująca `aiohttp` do wydajnej komunikacji z serwerami Telegram.

## 👤 Autor

**Denys Ostrovskyi**
- 📧 Email: [ostrovskyidenys30@gmail.com](mailto:ostrovskyidenys30@gmail.com)
- 💬 Telegram: [@denbas9](https://t.me/denbas9)
- 💼 GitHub: [@denys-ostrovskyi](https://github.com/Denba236)

## 📋 Spis treści

- [Funkcjonalności](#-funkcjonalności)
- [Wymagania](#-wymagania)
- [Instalacja](#-instalacja)
- [Szybki start](#-szybki-start)
- [Przykłady użycia](#-przykłady-użycia)
- [Zasady kodowania](#-zasady-kodowania)
- [Dokumentacja API](#-dokumentacja-api)
- [Benchmarki](#-benchmarki)
- [Struktura projektu](#-struktura-projektu)
- [Testowanie](#-testowanie)
- [Wielojęzyczność](#-wielojęzyczność)
- [Wkład w rozwój](#-wkład-w-rozwój)
- [Licencja](#-licencja)
- [Kontakt i wsparcie](#-kontakt-i-wsparcie)

## ✨ Funkcjonalności

- ✅ **W pełni asynchroniczna** - wykorzystuje async/await dla maksymalnej wydajności
- ✅ **Obsługa oficjalnego API Telegram** - pełna kompatybilność z Bot API
- ✅ **Zarządzanie sesjami** - automatyczne odnawianie połączeń
- ✅ **Obsługa webhooków** - łatwa konfiguracja odbierania aktualizacji
- ✅ **Wysyłanie multimediów** - zdjęcia, wideo, dokumenty, audio
- ✅ **Klawiatury inline i reply** - interaktywne wiadomości
- ✅ **Rate limiting** - automatyczne dostosowanie do limitów API
- ✅ **Pełne typowanie** - wsparcie dla IDE i type checkerów
- ✅ **Obsługa błędów** - zaawansowany system retry i obsługi wyjątków
- ✅ **Wielojęzyczność** - wsparcie dla różnych języków w odpowiedziach bota
- ✅ **Middleware** - system przetwarzania zapytań
- ✅ **Testy jednostkowe** - pokrycie kodu >90%

## 🔧 Wymagania

- Python 3.7 lub nowszy
- aiohttp >= 3.8.0
- Konto bota Telegram (token od [@BotFather](https://t.me/botfather))

## 📦 Instalacja

### Instalacja z PyPI
```bash
pip install telegram-async