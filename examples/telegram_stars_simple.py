"""
Prosty bot z płatnością 5 Telegram Stars
Minimalny przykład użycia Telegram Stars
"""
from telegram_async import Bot, Dispatcher, Router
from telegram_async.telegram_types.new_types import LabeledPrice


# ==================== KONFIGURACJA ====================
BOT_TOKEN = "YOUR_BOT_TOKEN"  # Zmień na swój token bota
# ======================================================

STARS_AMOUNT = 5
CURRENCY = "XTR"  # Telegram Stars

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
router = Router()


@router.command("start")
async def cmd_start(ctx):
    """Komenda start"""
    await ctx.reply(
        "👋 <b>Witaj!</b>\n\n"
        "⭐ Ten bot przyjmuje płatności w Telegram Stars.\n\n"
        "💰 Kwota: <b>5 Stars</b> ⭐\n\n"
        "Użyj /pay aby zapłacić 👇",
        parse_mode="HTML"
    )


@router.command("pay")
async def cmd_pay(ctx):
    """Wyślij fakturę 5 Telegram Stars"""
    await ctx.send_invoice(
        title="⭐ 5 Telegram Stars",
        description="Płatność za usługę premium",
        payload=f"stars_5_{ctx.user_id}",
        provider_token="",  # Puste dla Stars
        currency=CURRENCY,
        prices=[
            LabeledPrice(label="5 Telegram Stars", amount=STARS_AMOUNT)
        ]
    )


@router.pre_checkout_query()
async def pre_checkout(ctx):
    """Zaakceptuj płatność Stars"""
    await ctx.answer_pre_checkout_query(ok=True)


@router.successful_payment()
async def success_payment(ctx):
    """Obsługa udanej płatności Stars"""
    stars = ctx.successful_payment.total_amount
    
    await ctx.reply(
        f"✅ <b>Płatność zakończona sukcesem!</b>\n\n"
        f"⭐ Kwota: {stars} Telegram Stars\n"
        f"🆔 ID: {ctx.successful_payment.telegram_payment_charge_id}\n\n"
        f"Dziękujemy! 🌟",
        parse_mode="HTML"
    )


dp.include_router(router)

if __name__ == "__main__":
    print("=" * 50)
    print("⭐ Bot Telegram Stars - 5 Stars")
    print("=" * 50)
    print("\n💡 Konfiguracja:")
    print("  1. Zmień BOT_TOKEN na swój token")
    print("  2. NIE potrzebujesz PROVIDER_TOKEN!")
    print("  3. Waluta: XTR (Telegram Stars)")
    print("\n🚀 Uruchamianie...")
    print("=" * 50)
    
    dp.run_polling(bot)
