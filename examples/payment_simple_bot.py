"""
Prosty bot z płatnością 5 PLN
Minimalny przykład użycia Telegram Payments
"""
from telegram_async import Bot, Dispatcher, Router


# ==================== KONFIGURACJA ====================
BOT_TOKEN = "YOUR_BOT_TOKEN"  # Zmień na swój token bota
PROVIDER_TOKEN = "YOUR_PROVIDER_TOKEN"  # Token dostawcy płatności (np. Stripe)
# ======================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
router = Router()


@router.command("start")
async def cmd_start(ctx):
    """Komenda start"""
    await ctx.reply(
        "👋 <b>Witaj!</b>\n\n"
        "💰 Ten bot służy do przyjmowania płatności.\n\n"
        "Kwota: <b>5 PLN</b>\n\n"
        "Użyj /pay aby zapłacić 👇",
        parse_mode="HTML"
    )


@router.command("pay")
async def cmd_pay(ctx):
    """Wyślij fakturę 5 PLN"""
    await ctx.answer(
        title="Płatność 5 PLN",
        description="Opłata za usługę premium",
        payload="payment_5pln",
        provider_token=PROVIDER_TOKEN,
        currency="PLN",
        prices=[
            {"label": "Usługa Premium", "amount": 500}  # 5.00 PLN (w groszach)
        ],
        need_email=True
    )


@router.pre_checkout_query()
async def pre_checkout(ctx):
    """Zaakceptuj płatność"""
    await ctx.answer_pre_checkout_query(ok=True)


@router.successful_payment()
async def success_payment(ctx):
    """Obsługa udanej płatności"""
    amount = ctx.successful_payment.total_amount / 100
    
    await ctx.reply(
        f"✅ <b>Płatność zakończona sukcesem!</b>\n\n"
        f"💰 Kwota: {amount} PLN\n"
        f"🆔 ID: {ctx.successful_payment.telegram_payment_charge_id}\n\n"
        "Dziękujemy! 🎉",
        parse_mode="HTML"
    )


dp.include_router(router)

if __name__ == "__main__":
    print("🤖 Bot Płatności 5 PLN")
    print("Zmień BOT_TOKEN i PROVIDER_TOKEN w pliku!")
    dp.run_polling(bot)
