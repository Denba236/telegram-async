import asyncio
from telegram_async import Bot, Dispatcher, Context
from telegram_async.dispatcher.router import Router
# Inicjalizacja bota i dispatchera
bot = Bot("TOKEN")
dp = Dispatcher(bot)
user_router = Router(name="user_handlers")

user_language = {}
@user_router.command("start")
async def start_handler(ctx: Context):
   """Obsługa komendy /start przy użyciu routera"""
   user_id = ctx.user_id
   lang = user_language.get(user_id, "pl")
   await ctx.reply(f"Witaj, {ctx.message.from_user.first_name}! (Język: {lang})")
@user_router.message()
async def echo_handler(ctx: Context):

    if ctx.text == "/help":
     await ctx.reply("To jest pomoc obsługiwana przez router.")
    else:
        await ctx.reply(f"Otrzymałem: {ctx.text}")
@user_router.callback_query()
async def language_callback(ctx: Context):
    if ctx.callback_query.data.startswith("lang_"):
       lang = ctx.callback_query.data.replace("lang_", "")
       user_language[ctx.user_id] = lang
       await ctx.answer_callback(f"Zmieniono język na {lang}")
       await ctx.edit_message(f"Wybrany język: {lang}")

dp.include_router(user_router)

async def main():

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
