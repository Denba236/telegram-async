import asyncio
from telegram_async import Bot, Dispatcher
from telegram_async.filters import Command

BOT_TOKEN = "8158576821:AAFX-ZQ0qIJMwshtBnwXUOGXmHAw888A04s"  # Zastąp swoim tokenem
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(ctx):
    await ctx.reply("Cześć! Bot działa poprawnie! 🎉")

@dp.message(Command("help"))
async def help_handler(ctx):
    await ctx.reply(
        "Dostępne komendy:\n"
        "/start - powitanie\n"
        "/help - pomoc\n"
        "/test - test importów"
    )

@dp.message(Command("test"))
async def test_handler(ctx):
    from telegram_async.telegram_types import User, Message
    await ctx.reply("✅ Importy działają poprawnie!")

@dp.message()
async def echo_handler(ctx):
    if ctx.message.text:
        await ctx.reply(f"Otrzymałem: {ctx.message.text}")
    else:
        await ctx.reply("Otrzymałem wiadomość")

async def main():
    print("Bot uruchomiony...")
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("\nBot zatrzymany.")

if __name__ == "__main__":
    asyncio.run(main())