import asyncio
from telegram_async import Bot, Dispatcher, types
from telegram_async.filters import Command

# Inicjalizacja
bot = Bot("YOUR_BOT_TOKEN")
dp = Dispatcher()

# Handler komendy /start
@dp.message(Command("start"))
async def start_handler(ctx):
    await ctx.reply(
        "👋 Witaj! Jestem botem echo.\n"
        "Wyślij mi dowolną wiadomość, a ją powtórzę.\n"
        "Komendy: /help, /info"
    )

# Handler komendy /help
@dp.message(Command("help"))
async def help_handler(ctx):
    await ctx.reply(
        "📚 Dostępne komendy:\n"
        "/start - rozpoczęcie\n"
        "/help - pomoc\n"
        "/info - info o bocie\n"
        "/echo <tekst> - powtórz tekst"
    )

# Handler komendy /info
@dp.message(Command("info"))
async def info_handler(ctx):
    user = ctx.message.from_user
    await ctx.reply(
        f"📊 Informacje:\n"
        f"Twój ID: {user.id}\n"
        f"Username: @{user.username}\n"
        f"Imię: {user.first_name}\n"
        f"Czat ID: {ctx.chat_id}"
    )

# Handler komendy /echo
@dp.message(Command("echo"))
async def echo_command_handler(ctx):
    # Pobierz tekst po komendzie
    text = ctx.message.text.replace("/echo", "", 1).strip()
    if text:
        await ctx.reply(f"📢 Echo: {text}")
    else:
        await ctx.reply("❌ Podaj tekst do powtórzenia. Przykład: /echo Hello World!")

# Handler dla wszystkich wiadomości (echo)
@dp.message()
async def echo_handler(ctx):
    if ctx.message.text:
        await ctx.reply(f"✉️ Powtarzam: {ctx.message.text}")
    elif ctx.message.photo:
        await ctx.reply("📸 Otrzymałem zdjęcie!")
    elif ctx.message.sticker:
        await ctx.reply("😊 Otrzymałem naklejkę!")
    else:
        await ctx.reply("❓ Otrzymałem wiadomość, ale nie wiem co to jest.")

async def main():
    print("🤖 Bot uruchomiony...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())