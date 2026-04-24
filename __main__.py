"""
Allow running telegram_async as a module:
    python -m telegram_async init my_bot
    python -m telegram_async list-templates
"""
from .cli import main

main()
