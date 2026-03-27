from telegram_async import Bot, Dispatcher
from telegram_async.i18n import I18n

# Initialize the translation system
i18n = I18n("locales/")
bot = Bot("TOKEN")

# User language dictionary
user_language = {}


@bot.on_message
async def handle_message(message):
    # Language detection (previously saved or default)
    user_id = message.from_user.id if message.from_user else 0
    lang = user_language.get(user_id, "pl")

    if message.text == "/start":
        # Greeting translation
        text = i18n.get(lang, "welcome", name=message.from_user.first_name)
        await bot.send_message(message.chat.id, text)

    elif message.text == "/help":
        help_text = i18n.get(lang, "help_message")
        await bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

    elif message.text == "/lang":
        # Change language
        keyboard = InlineKeyboard([
            [InlineButton("🇵🇱 Polski", callback_data="lang_pl")],
            [InlineButton("🇬🇧 English", callback_data="lang_en")],
            [InlineButton("🇷🇺 Русский", callback_data="lang_ru")]
        ])
        await bot.send_message(
            message.chat.id,
            "Choose language:",
            reply_markup=keyboard
        )


@bot.on_callback_query
async def handle_language(callback):
    if callback.data.startswith("lang_"):
        lang = callback.data.replace("lang_", "")
        user_language[callback.from_user.id] = lang

        await bot.answer_callback_query(
            callback.id,
            text=i18n.get(lang, "language_changed")
        )

        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=i18n.get(lang, "language_set")
        )