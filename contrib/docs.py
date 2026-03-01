from typing import Dict, Any, Optional, List
import inspect


def generate_help(dispatcher) -> str:
    """
    Generuje tekst help z listą komend i minimalną info

    Args:
        dispatcher: Instancja Dispatcher z zarejestrowanymi handlerami

    Returns:
        Sformatowany tekst pomocy
    """
    lines = ["📖 **Lista komend:**\n"]

    # Zbierz komendy z dispatchera
    commands = dispatcher.handlers.get('command', {})

    for cmd, handler in commands.items():
        # Sprawdź czy handler ma docstring
        doc = inspect.getdoc(handler)
        description = doc.split('\n')[0] if doc else "Brak opisu"

        # Sprawdź czy wymaga roli
        required_role = getattr(handler, '__required_role__', None)
        role_info = f" [wymaga: {required_role}]" if required_role else ""

        lines.append(f"  /{cmd} - {description}{role_info}")

    return "\n".join(lines)


async def send_help(ctx, dispatcher):
    """
    Wysyła pomoc do czatu

    Args:
        ctx: Kontekst handlera
        dispatcher: Instancja Dispatcher
    """
    help_text = generate_help(dispatcher)
    await ctx.reply(help_text, parse_mode="Markdown")


def generate_commands_list(dispatcher) -> List[Dict[str, Any]]:
    """
    Generuje listę komend dla BotFather (setMyCommands)

    Args:
        dispatcher: Instancja Dispatcher

    Returns:
        Lista słowników z komendami i opisami
    """
    commands = []

    for cmd, handler in dispatcher.handlers.get('command', {}).items():
        doc = inspect.getdoc(handler)
        description = doc.split('\n')[0] if doc else "Brak opisu"

        # Ogranicz do 256 znaków
        description = description[:256]

        commands.append({
            "command": cmd,
            "description": description
        })

    return commands