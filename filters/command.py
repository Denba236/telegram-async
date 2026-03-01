def Command(name: str):
    """
    Filtr dla komendy /name

    Przykład:
        @dp.message(Command("start"))
        async def start_handler(ctx):
            await ctx.reply("Cześć!")
    """

    async def filter_func(message):
        if not message.text:
            return False
        if not message.text.startswith('/'):
            return False

        cmd = message.text.split()[0][1:].lower()
        if '@' in cmd:
            cmd = cmd.split('@')[0]

        return cmd == name.lower()

    return filter_func