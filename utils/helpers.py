import re
from typing import Optional, List


def parse_command(text: str) -> tuple[Optional[str], Optional[str]]:
    """
    Parsuje komendę z tekstu
    Returns: (command, args)
    """
    if not text or not text.startswith('/'):
        return None, None

    parts = text.split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else None

    # Usuń @username z komendy jeśli jest
    if '@' in command:
        command = command.split('@')[0]

    return command, args


def split_text(text: str, max_length: int = 4096) -> List[str]:
    """
    Dzieli tekst na fragmenty nie dłuższe niż max_length
    """
    if len(text) <= max_length:
        return [text]

    parts = []
    while text:
        if len(text) <= max_length:
            parts.append(text)
            break

        # Znajdź miejsce podziału (ostatnia spacja)
        split_at = text.rfind(' ', 0, max_length)
        if split_at == -1:
            split_at = max_length

        parts.append(text[:split_at])
        text = text[split_at:].lstrip()

    return parts


def escape_markdown(text: str, version: int = 2) -> str:
    """
    Escape'uje znaki specjalne Markdown
    """
    if version == 2:
        chars = r'_*[]()~`>#+-=|{}.!'
    else:
        chars = r'_*`['

    return re.sub(f'([{re.escape(chars)}])', r'\\\1', text)


def build_menu(
        buttons: List[str],
        n_cols: int = 2,
        header_buttons: Optional[List[str]] = None,
        footer_buttons: Optional[List[str]] = None
) -> List[List[str]]:
    """
    Buduje menu z listy przycisków
    """
    menu = []

    if header_buttons:
        menu.append(header_buttons)

    rows = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    menu.extend(rows)

    if footer_buttons:
        menu.append(footer_buttons)

    return menu


def extract_entities(text: str, entities: List) -> dict:
    """
    Wyodrębnia encje z tekstu (np. linki, mention)
    """
    result = {}
    for entity in entities:
        if entity.type == 'url':
            result['url'] = text[entity.offset:entity.offset + entity.length]
        elif entity.type == 'bot_command':
            result['command'] = text[entity.offset:entity.offset + entity.length]
        elif entity.type == 'mention':
            result['mention'] = text[entity.offset:entity.offset + entity.length]
        elif entity.type == 'hashtag':
            result['hashtag'] = text[entity.offset:entity.offset + entity.length]
    return result