"""
Bot z płatnością Telegram Stars - 5 Stars
Przykład użycia Telegram Stars (API 9.5+)

Telegram Stars to wewnętrzna waluta Telegrama.
Użytkownicy kupują Stars i płacą nimi w botach.
"""
from telegram_async import Bot, Dispatcher, Router
from telegram_async.telegram_types.new_types import LabeledPrice


# ==================== KONFIGURACJA ====================
BOT_TOKEN = "TOKEN"  # Zmień na swój token bota
# ======================================================

# Telegram Stars używa specjalnej waluty "XTR"
STARS_AMOUNT = 5  # 5 Telegram Stars
CURRENCY = "XTR"  # Telegram Stars currency code

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
router = Router()


@router.command("start")
async def cmd_start(ctx):
    """Komenda start"""
    welcome_text = (
        "⭐ <b>Bot Telegram Stars</b>\n\n"
        "🌟 Ten bot przyjmuje płatności w Telegram Stars!\n\n"
        "💰 <b>Cena:</b> 5 Stars ⭐\n\n"
        "🎁 <b>Co otrzymasz?</b>\n"
        "• ✅ Dostęp do funkcji premium\n"
        "• ✅ Specjalne komendy\n"
        "• ✅ Wsparcie developera\n\n"
        "👇 Kliknij /pay aby zapłacić!"
    )
    
    await ctx.reply(text=welcome_text, parse_mode="HTML")


@router.command("pay")
async def cmd_pay(ctx):
    """Wyślij fakturę 5 Telegram Stars"""
    await ctx.send_invoice(
        title="⭐ 5 Telegram Stars",
        description=(
            "🌟 Płatność 5 Telegram Stars\n\n"
            "✅ Aktywacja konta Premium\n"
            "✅ Dostęp do specjalnych funkcji\n"
            "✅ Wsparcie developera\n\n"
            "Płatność przez Telegram Stars ⭐"
        ),
        payload=f"stars_payment_{ctx.user_id}",
        # W walucie Telegram Stars NIE potrzebujesz provider_token!
        provider_token="",  # Puste dla XTR
        currency=CURRENCY,
        prices=[
            LabeledPrice(label="5 Telegram Stars", amount=STARS_AMOUNT)
        ],
        need_email=False,  # Stars nie wymagają email
        need_name=False,   # Ani imienia
        need_phone_number=False
    )


@router.pre_checkout_query()
async def pre_checkout_handler(ctx):
    """
    Walidacja płatności przed potwierdzeniem
    Dla Telegram Stars - zawsze akceptujemy
    """
    # Sprawdź czy payload jest poprawny
    if not ctx.invoice_payload.startswith("stars_payment_"):
        await ctx.answer_pre_checkout_query(
            ok=False,
            error_message="❌ Nieprawidłowa płatność"
        )
        return
    
    # Sprawdź czy użytkownik nie jest zbanowany
    # Tutaj możesz dodać własną logikę
    
    # Zaakceptuj płatność
    await ctx.answer_pre_checkout_query(ok=True)
    print(f"✅ Płatność Stars zaakceptowana dla użytkownika {ctx.user_id}")


@router.successful_payment()
async def successful_payment_handler(ctx):
    """
    Obsługa udanej płatności Stars
    """
    payment = ctx.successful_payment
    
    # Pobierz informacje o płatności
    stars_amount = payment.total_amount  # W Telegram Stars
    payment_currency = payment.currency  # "XTR"
    
    # Tutaj zapisz płatność do bazy danych
    # await database.save_payment(
    #     user_id=ctx.user_id,
    #     amount=stars_amount,
    #     currency=payment_currency,
    #     telegram_payment_charge_id=payment.telegram_payment_charge_id,
    #     provider_payment_charge_id=payment.provider_payment_charge_id
    # )
    
    # Aktywuj Premium dla użytkownika
    # await database.activate_premium(ctx.user_id, days=30)
    
    # Podziękowanie
    success_message = (
        "🎉 <b>Płatność Stars zakończona sukcesem!</b>\n\n"
        f"⭐ Kwota: <b>{stars_amount} Telegram Stars</b>\n"
        f"🆔 ID transakcji: <code>{payment.telegram_payment_charge_id}</code>\n\n"
        "✅ <b>Twoje konto Premium jest aktywne!</b>\n\n"
        "🌟 Korzystaj ze wszystkich funkcji premium!\n\n"
        "Dziękujemy za wsparcie! ⭐"
    )
    
    # Wyślij potwierdzenie
    await ctx.reply(text=success_message, parse_mode="HTML")
    
    print(f"⭐ Otrzymano {stars_amount} Stars od użytkownika {ctx.user_id}")


@router.command("premium")
async def cmd_premium(ctx):
    """Pokazuje informacje o Premium"""
    text = (
        "⭐ <b>Dlaczego Telegram Stars?</b>\n\n"
        "🌟 <b>Łatwe płatności:</b>\n"
        "• Nie potrzebujesz karty kredytowej\n"
        "• Płacisz przez Telegram\n"
        "• Szybko i bezpiecznie\n\n"
        "💎 <b>Korzyści z Premium:</b>\n"
        "• ✅ Wszystkie funkcje premium\n"
        "• ✅ Specjalne komendy\n"
        "• ✅ Priorytetowe wsparcie\n\n"
        "💰 <b>Cena: 5 Stars</b>\n\n"
        "👇 Użyj /pay aby zapłacić!"
    )
    
    await ctx.reply(text=text, parse_mode="HTML")


@router.command("stars")
async def cmd_stars_info(ctx):
    """Informacje o Telegram Stars"""
    text = (
        "⭐ <b>Co to są Telegram Stars?</b>\n\n"
        "🌟 Telegram Stars to wewnętrzna waluta Telegrama\n\n"
        "💰 <b>Jak kupić Stars?</b>\n"
        "1. Otwórz Ustawienia Telegram\n"
        "2. Kliknij \"Telegram Stars\"\n"
        "3. Wybierz pakiet\n"
        "4. Zapłać kartą\n\n"
        "💡 <b>Ile kosztuje 5 Stars?</b>\n"
        "• 1 Star ≈ $0.013 USD\n"
        "• 5 Stars ≈ $0.065 USD (ok. 0.25 PLN)\n\n"
        "🎁 <b>Co mogę zrobić ze Stars?</b>\n"
        "• Płacić w botach\n"
        "• Kupować produkty cyfrowe\n"
        "• Wspierać twórców\n\n"
        "👇 Użyj /pay aby zapłacić 5 Stars!"
    )
    
    await ctx.reply(text=text, parse_mode="HTML")


@router.message()
async def echo_all(ctx):
    """Domyślna obsługa wiadomości"""
    text = ctx.text
    
    if text:
        if "premium" in text.lower() or "stars" in text.lower():
            await cmd_stars_info(ctx)
        else:
            await ctx.reply(
                "🤔 Nie rozumiem tej komendy.\n\n"
                "Dostępne komendy:\n"
                "• /start - Powitanie\n"
                "• /pay - Zapłać 5 Stars\n"
                "• /premium - Informacje o Premium\n"
                "• /stars - Co to są Stars?"
            )


# Dołącz router do dispatcher
dp.include_router(router)


if __name__ == "__main__":
    print("=" * 60)
    print("⭐ Bot Telegram Stars - Płatność 5 Stars")
    print("=" * 60)
    print("\n📋 Komendy:")
    print("  /start   - Powitanie")
    print("  /pay     - Zapłać 5 Stars")
    print("  /premium - Informacje o Premium")
    print("  /stars   - Co to są Telegram Stars?")
    print("\n💡 Konfiguracja:")
    print("  1. Zmień BOT_TOKEN na swój token z @BotFather")
    print("  2. NIE potrzebujesz PROVIDER_TOKEN!")
    print("  3. Uruchom bota: python telegram_stars_bot.py")
    print("\n🌟 Telegram Stars:")
    print("  - Waluta: XTR (Telegram Stars)")
    print("  - Brak dostawcy płatności (provider)")
    print("  - Płatność przez Telegram")
    print("=" * 60)
    
    # Uruchomienie bota
    print("\n🚀 Uruchamianie bota...")
    dp.run_polling(bot)
