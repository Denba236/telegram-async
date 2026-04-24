"""
Bot Telegram Premium - Aktywacja na 1 miesiąc
Bot przyjmuje płatność w Telegram Stars i aktywuje Premium

UWAGA: Bot NIE może bezpośrednio aktywować Premium.
Zamiast tego przyjmuje płatność i daje instrukcję aktywacji.
"""
from telegram_async import Bot, Dispatcher, Router
from telegram_async.telegram_types.new_types import LabeledPrice


# ==================== KONFIGURACJA ====================
BOT_TOKEN = "TOKEN"  # Zmień na swój token

# Cena Telegram Premium (około 250 Stars = ~1 miesiąc)
# Sprawdź aktualną cenę w Telegramie
PREMIUM_STARS = 30  # 1 Star - wersja testowa
CURRENCY = "XTR"  # Telegram Stars
# ======================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
router = Router()


@router.command("start")
async def cmd_start(ctx):
    """Komenda start - powitanie i oferta Premium"""
    welcome_text = (
        "🌟 <b>Telegram Premium Bot</b>\n\n"
        "🎁 Aktywuj Telegram Premium na <b>1 miesiąc</b>!\n\n"
        "💎 <b>Korzyści z Premium:</b>\n"
        "• ✅ Limit 2000 MB na pliki (zamiast 50 MB)\n"
        "• ✅ Pobieranie bez limitu prędkości\n"
        "• ✅ Konwersja głosu na tekst\n"
        "• ✅ Brak reklam\n"
        "• ✅ Reakcje na wiadomości\n"
        "• ✅ Zaawansowane zarządzanie czatem\n"
        "• ✅ I wiele więcej!\n\n"
        "💰 <b>Cena: 250 Stars</b> ⭐\n"
        "(około $3.25 USD / ~13 PLN)\n\n"
        "👇 Użyj /premium aby aktywować!"
    )
    
    await ctx.reply(text=welcome_text, parse_mode="HTML")


@router.command("premium")
async def cmd_premium(ctx):
    """Wyślij fakturę za Premium"""
    invoice_text = (
        "🌟 <b>Telegram Premium - 1 Miesiąc</b>\n\n"
        "📅 Ważność: 30 dni\n"
        "⭐ Cena: 250 Stars\n\n"
        "Po płatności otrzymasz instrukcję aktywacji.\n\n"
        "💡 <b>Jak zapłacić?</b>\n"
        "1. Kliknij przycisk poniżej\n"
        "2. Potwierdź płatność Stars\n"
        "3. Gotowe! Otrzymasz instrukcję"
    )
    
    await ctx.send_invoice(
        title="🌟 Telegram Premium (1 miesiąc)",
        description=(
            "Aktywacja Telegram Premium na 30 dni\n\n"
            "Korzyści:\n"
            "• Limit plików 2000 MB\n"
            "• Szybsze pobieranie\n"
            "• Transkrypcja głosu\n"
            "• Brak reklam\n"
            "• Reakcje\n"
            "• I więcej!"
        ),
        payload=f"premium_{ctx.user_id}_1month",
        provider_token="",  # Puste dla Stars
        currency=CURRENCY,
        prices=[
            LabeledPrice(
                label="Telegram Premium - 1 miesiąc",
                amount=PREMIUM_STARS
            )
        ],
        need_email=False,
        need_name=False,
        need_phone_number=False
    )
    
    await ctx.reply(text=invoice_text, parse_mode="HTML")


@router.pre_checkout_query()
async def pre_checkout_handler(ctx):
    """Walidacja płatności Premium"""
    payload = ctx.invoice_payload
    
    # Sprawdź czy payload jest poprawny
    if not payload.startswith("premium_"):
        await ctx.answer_pre_checkout_query(
            ok=False,
            error_message="❌ Nieprawidłowa płatność"
        )
        return
    
    # Sprawdź czy użytkownik nie ma już aktywnego Premium
    # Tutaj można dodać sprawdzenie w bazie danych
    # if await database.has_active_premium(ctx.user_id):
    #     await ctx.answer_pre_checkout_query(
    #         ok=False,
    #         error_message="Masz już aktywne Premium!"
    #     )
    #     return
    
    # Zaakceptuj płatność
    await ctx.answer_pre_checkout_query(ok=True)


@router.successful_payment()
async def successful_payment_handler(ctx):
    """Obsługa udanej płatności Premium"""
    payment = ctx.successful_payment
    
    # Pobierz informacje o płatności
    stars_paid = payment.total_amount
    transaction_id = payment.telegram_payment_charge_id
    
    # Tutaj zapisz płatność do bazy danych
    # await database.save_premium_activation(
    #     user_id=ctx.user_id,
    #     stars=stars_paid,
    #     transaction_id=transaction_id,
    #     valid_until=datetime.now() + timedelta(days=30)
    # )
    
    # Wiadomość potwierdzająca z instrukcją
    success_message = (
        "🎉 <b>Płatność zakończona sukcesem!</b>\n\n"
        f"⭐ Zapłacono: <b>{stars_paid} Stars</b>\n"
        f"🆔 ID transakcji: <code>{transaction_id}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "🌟 <b>Jak aktywować Telegram Premium?</b>\n\n"
        "📱 <b>Na telefonie:</b>\n"
        "1. Otwórz Ustawienia Telegram\n"
        "2. Kliknij \"Telegram Premium\"\n"
        "3. Kliknij \"Activate Gift\" lub \"Aktywuj kod\"\n"
        "4. Premium zostanie aktywowany!\n\n"
        "💻 <b>Na komputerze:</b>\n"
        "1. Otwórz Ustawienia → Premium\n"
        "2. Postępuj zgodnie z instrukcjami\n\n"
        "📅 <b>Ważność:</b> 30 dni od aktywacji\n\n"
        "❓ <b>Potrzebujesz pomocy?</b>\n"
        "Napisz do supportu: @PremiumSupport\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "✨ Ciesz się Telegram Premium!"
    )
    
    await ctx.reply(text=success_message, parse_mode="HTML")
    
    print(f"🌟 Premium aktywowany! {stars_paid} Stars od użytkownika {ctx.user_id}")


@router.command("help")
async def cmd_help(ctx):
    """Pomoc"""
    help_text = (
        "🆘 <b>Pomoc - Telegram Premium</b>\n\n"
        "📋 <b>Dostępne komendy:</b>\n"
        "• /start - Powitanie\n"
        "• /premium - Kup Premium (250 Stars)\n"
        "• /help - Ta wiadomość\n"
        "• /status - Sprawdź status Premium\n\n"
        "💡 <b>Jak kupić Premium?</b>\n"
        "1. Użyj /premium\n"
        "2. Zapłać 250 Stars\n"
        "3. Aktywuj w Ustawieniach Telegram\n\n"
        "❓ <b>Pytania?</b>\n"
        "Napisz do: @PremiumSupport"
    )
    
    await ctx.reply(text=help_text, parse_mode="HTML")


@router.command("status")
async def cmd_status(ctx):
    """Sprawdź status Premium"""
    # Tutaj sprawdź w bazie danych czy użytkownik ma Premium
    # premium_info = await database.get_premium_status(ctx.user_id)
    
    # Symulacja - zawsze pokaż że nie ma Premium
    status_text = (
        "📊 <b>Status Premium</b>\n\n"
        "❌ <b>Nie masz aktywnego Premium</b>\n\n"
        "💰 <b>Cena:</b> 250 Stars / miesiąc\n\n"
        "👇 Użyj /premium aby aktywować!"
    )
    
    await ctx.reply(text=status_text, parse_mode="HTML")


@router.message()
async def echo_all(ctx):
    """Domyślna obsługa wiadomości"""
    text = ctx.text
    
    if text:
        if "premium" in text.lower():
            await cmd_premium(ctx)
        elif "pomoc" in text.lower() or "help" in text.lower():
            await cmd_help(ctx)
        else:
            await ctx.reply(
                "🤖 <b>Telegram Premium Bot</b>\n\n"
                "Użyj /premium aby kupić Telegram Premium\n\n"
                "Komendy:\n"
                "• /start - Powitanie\n"
                "• /premium - Kup Premium\n"
                "• /help - Pomoc\n"
                "• /status - Sprawdź status",
                parse_mode="HTML"
            )


# Dołącz router do dispatcher
dp.include_router(router)


if __name__ == "__main__":
    print("=" * 60)
    print("🌟 Bot Telegram Premium - 1 Miesiąc")
    print("=" * 60)
    print("\n📋 Komendy:")
    print("  /start    - Powitanie")
    print("  /premium  - Kup Premium (250 Stars)")
    print("  /help     - Pomoc")
    print("  /status   - Sprawdź status")
    print("\n💡 Konfiguracja:")
    print("  1. Zmień BOT_TOKEN na swój token z @BotFather")
    print("  2. Ustaw cenę: 250 Stars (około $3.25)")
    print("  3. Uruchom: python premium_bot.py")
    print("\n⚠️ WAŻNE:")
    print("  Bot NIE aktywuje Premium automatycznie!")
    print("  Użytkownik musi aktywować Premium ręcznie")
    print("  w Ustawieniach Telegram")
    print("=" * 60)
    
    print("\n🚀 Uruchamianie bota...")
    dp.run_polling(bot)
