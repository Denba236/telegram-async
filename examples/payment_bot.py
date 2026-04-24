"""
Bot z płatnością - przykład użycia Telegram Payments
Bot prosi o opłatę 5 PLN za dostęp do usług premium.
"""
from telegram_async import Bot, Dispatcher, Router, StatesGroup, State
from telegram_async.keyboards.inline import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_async.telegram_types.new_types import LabeledPrice
import asyncio


# Stany FSM dla procesu płatności
class PaymentState(StatesGroup):
    WAITING_PAYMENT = State("waiting_payment")
    PAYMENT_SUCCESS = State("payment_success")
    PAYMENT_FAILED = State("payment_failed")


# Konfiguracja
BOT_TOKEN = "TOKEN"  # Zmień na swój token
PROVIDER_TOKEN = "YOUR_PROVIDER_TOKEN"  # Token dostawcy płatności (np. Stripe)
PAYMENT_AMOUNT = 500  # 5.00 PLN (w groszach - 5 * 100)
CURRENCY = "PLN"


# Tworzenie bota i dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
router = Router()


def create_payment_keyboard():
    """Tworzy klawiaturę z przyciskiem płatności"""
    # Przycisk płatności - musi być w reply_markup jako Invoice
    keyboard = InlineKeyboardMarkup()
    
    # Przycisk do zakupu
    pay_button = InlineKeyboardButton(
        text="💳 Zapłać 5 PLN",
        pay=True  # To tworzy przycisk płatności!
    )
    keyboard.add_button(pay_button)
    
    # Dodatkowe przyciski
    help_button = InlineKeyboardButton(
        text="❓ Pomoc",
        callback_data="help"
    )
    status_button = InlineKeyboardButton(
        text="📊 Status płatności",
        callback_data="check_status"
    )
    
    keyboard.add_row(help_button, status_button)
    
    return keyboard


def create_invoice_parameters():
    """Tworzy parametry faktury dla płatności"""
    return {
        'title': "Dostęp Premium",
        'description': (
            "🌟 Aktywuj konto Premium\n\n"
            "✅ Dostęp do wszystkich funkcji\n"
            "✅ Priorytetowe wsparcie\n"
            "✅ Brak reklam\n"
            "✅ Dodatkowe komendy\n\n"
            "Cena: 5 PLN / miesiąc"
        ),
        'payload': "premium_subscription_5pln",
        'provider_token': PROVIDER_TOKEN,
        'currency': CURRENCY,
        'prices': [
            LabeledPrice(label="Dostęp Premium (1 miesiąc)", amount=PAYMENT_AMOUNT)
        ],
        'start_parameter': "premium_payment",
        'photo_url': None,  # Opcjonalnie: URL zdjęcia produktu
        'photo_size': None,
        'photo_width': None,
        'photo_height': None,
        'need_name': False,
        'need_phone_number': False,
        'need_email': True,  # Pobierz email użytkownika
        'need_shipping_address': False,
        'is_flexible': False
    }


@router.command("start")
async def cmd_start(ctx):
    """Komenda start - powitanie i informacja o płatności"""
    welcome_text = (
        "👋 <b>Witaj w bocie Premium!</b>\n\n"
        "🤖 Jestem botem z funkcjami premium.\n\n"
        "💰 <b>Cennik:</b>\n"
        "• Dostęp Premium: <b>5 PLN/miesiąc</b>\n\n"
        "🎁 <b>Korzyści z Premium:</b>\n"
        "• ✅ Wszystkie funkcje odblokowane\n"
        "• ✅ Szybsze odpowiedzi\n"
        "• ✅ Priorytetowe wsparcie 24/7\n"
        "• ✅ Brak limitów\n\n"
        "Użyj /pay aby dokonać płatności lub kliknij przycisk poniżej 👇"
    )
    
    await ctx.reply(
        text=welcome_text,
        parse_mode="HTML",
        reply_markup=create_payment_keyboard()
    )


@router.command("pay")
async def cmd_pay(ctx):
    """Komenda płatności - wysyła fakturę"""
    # Pobierz parametry faktury
    invoice_params = create_invoice_parameters()
    
    # Wyślij fakturę
    await ctx.send_invoice(**invoice_params)
    
    await ctx.reply(
        "📧 Sprawdź wiadomość od bota z fakturą i kliknij \"Zapłać\"\n\n"
        "💡 Możesz też kliknąć przycisk \"💳 Zapłać 5 PLN\" powyżej"
    )


@router.command("premium")
async def cmd_premium(ctx):
    """Pokazuje informacje o Premium"""
    text = (
        "🌟 <b>Dlaczego warto mieć Premium?</b>\n\n"
        "1️⃣ <b>Pełny dostęp</b>\n"
        "   Wszystkie funkcje są odblokowane\n\n"
        "2️⃣ <b>Szybkość</b>\n"
        "   Priorytetowe przetwarzanie zapytań\n\n"
        "3️⃣ <b>Wsparcie</b>\n"
        "   Pomoc techniczna 24/7\n\n"
        "4️⃣ <b>Bez limitów</b>\n"
        "   Bez ograniczeń w użytkowaniu\n\n"
        "💳 <b>Tylko 5 PLN miesięcznie!</b>\n\n"
        "Użyj /pay aby aktywować Premium ✨"
    )
    
    await ctx.reply(text=text, parse_mode="HTML")


@router.callback_query(lambda c: c.data == "help")
async def callback_help(ctx):
    """Obsługa przycisku pomocy"""
    help_text = (
        "🆘 <b>Pomoc - Płatności</b>\n\n"
        "📝 <b>Jak zapłacić?</b>\n"
        "1. Kliknij /pay lub przycisk \"💳 Zapłać\"\n"
        "2. Otrzymasz fakturę w wiadomości\n"
        "3. Kliknij \"Zapłać\" na fakturze\n"
        "4. Podaj dane karty kredytowej\n"
        "5. Gotowe! 🎉\n\n"
        "💳 <b>Akceptowane metody płatności:</b>\n"
        "• Karty Visa/Mastercard\n"
        "• Apple Pay\n"
        "• Google Pay\n\n"
        "❓ Masz pytania? Skontaktuj się z nami!"
    )
    
    await ctx.answer_callback_query(
        text="📖 Informacje o płatnościach",
        show_alert=False
    )
    
    await ctx.reply(text=help_text, parse_mode="HTML")


@router.callback_query(lambda c: c.data == "check_status")
async def callback_check_status(ctx):
    """Sprawdzanie statusu płatności"""
    # Tutaj można sprawdzić w bazie danych czy użytkownik ma Premium
    user_id = ctx.user_id
    
    # Symulacja sprawdzenia
    # W prawdziwym bocie: status = await database.get_user_subscription(user_id)
    is_premium = False  # Zmień na prawdziwe sprawdzenie
    
    if is_premium:
        status_text = (
            "✅ <b>Twoje konto ma aktywny status Premium!</b>\n\n"
            "📅 Ważność: 30 dni\n"
            "💰 Kwota: 5 PLN\n\n"
            "🎉 Korzystaj ze wszystkich funkcji!"
        )
    else:
        status_text = (
            "❌ <b>Nie masz aktywnego Premium</b>\n\n"
            "💰 Cena: <b>5 PLN/miesiąc</b>\n\n"
            "Użyj /pay aby aktywować Premium i uzyskać:\n"
            "✅ Pełny dostęp\n"
            "✅ Priorytetowe wsparcie\n"
            "✅ Brak limitów"
        )
    
    await ctx.answer_callback_query(
        text="📊 Sprawdzanie statusu...",
        show_alert=False
    )
    
    await ctx.reply(text=status_text, parse_mode="HTML")


@router.pre_checkout_query()
async def pre_checkout_handler(ctx):
    """
    Obsługa zapytania przed płatnością
    To jest wywoływane zanim użytkownik potwierdzi płatność
    """
    # Sprawdź poprawność płatności
    # Możesz sprawdzić:
    # - Czy payload jest poprawny
    # - Czy cena się zgadza
    # - Czy użytkownik nie jest zbanowany
    
    try:
        # Tutaj możesz dodać własną logikę walidacji
        # np. sprawdzenie czy użytkownik już nie ma Premium
        
        # Zaakceptuj płatność
        await ctx.answer_pre_checkout_query(
            ok=True,
            error_message=None
        )
        
        print(f"✅ Płatność zaakceptowana dla użytkownika {ctx.user_id}")
        
    except Exception as e:
        # Odrzuć płatność w przypadku błędu
        await ctx.answer_pre_checkout_query(
            ok=False,
            error_message=f"Błąd płatności: {str(e)}"
        )


@router.successful_payment()
async def successful_payment_handler(ctx):
    """
    Obsługa udanej płatności
    Wywoływane gdy płatność zakończyła się sukcesem
    """
    payment = ctx.successful_payment
    
    # Pobierz informacje o płatności
    payment_amount = payment.total_amount / 100  # Konwersja z groszy na złote
    payment_currency = payment.currency
    user_payload = payment.invoice_payload
    
    # Tutaj zapisz płatność do bazy danych
    # await database.save_payment(
    #     user_id=ctx.user_id,
    #     amount=payment_amount,
    #     currency=payment_currency,
    #     telegram_payment_charge_id=payment.telegram_payment_charge_id,
    #     provider_payment_charge_id=payment.provider_payment_charge_id
    # )
    
    # Aktywuj Premium dla użytkownika
    # await database.activate_premium(ctx.user_id, days=30)
    
    # Podziękowanie za płatność
    success_message = (
        "🎉 <b>Płatność zakończona sukcesem!</b>\n\n"
        f"💰 Kwota: <b>{payment_amount} {payment_currency}</b>\n"
        f"🆔 ID transakcji: <code>{payment.telegram_payment_charge_id}</code>\n\n"
        "✅ <b>Twoje konto Premium jest teraz aktywne!</b>\n\n"
        "🌟 Korzystaj ze wszystkich funkcji:\n"
        "• ✅ Brak limitów\n"
        "• ✅ Priorytetowe wsparcie\n"
        "• ✅ Wszystkie funkcje premium\n\n"
        "📅 Premium wygaśnie za 30 dni\n\n"
        "Dziękujemy za wspar! 💙"
    )
    
    # Wyślij wiadomość z potwierdzeniem
    await ctx.reply(text=success_message, parse_mode="HTML")
    
    # Opcjonalnie: wyślij potwierdzenie na email
    # if ctx.message.from_user.username:
    #     await send_email_confirmation(ctx.message.from_user)
    
    print(f"💰 Płatność {payment_amount} {payment_currency} od użytkownika {ctx.user_id}")


@router.message()
async def echo_all(ctx):
    """Domyślna obsługa wiadomości"""
    text = ctx.text
    
    if text:
        if "premium" in text.lower() or "płatn" in text.lower():
            await cmd_premium(ctx)
        else:
            await ctx.reply(
                "🤔 Nie rozumiem tej komendy.\n\n"
                "Użyj /start aby zobaczyć dostępne opcje\n"
                "Lub /pay aby dokonać płatności (5 PLN)"
            )


# Dołącz router do dispatcher
dp.include_router(router)


if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Bot Premium - Płatność 5 PLN")
    print("=" * 50)
    print("\n📋 Komendy:")
    print("  /start     - Powitanie i informacje")
    print("  /pay       - Dokonaj płatności")
    print("  /premium   - Informacje o Premium")
    print("\n💡 Konfiguracja:")
    print("  1. Zmień BOT_TOKEN na swój token z @BotFather")
    print("  2. Zmień PROVIDER_TOKEN na token dostawcy płatności")
    print("  3. Uruchom bota: python payment_bot.py")
    print("\n🔗 Provider token uzyskasz u dostawcy płatności:")
    print("   - Stripe: https://stripe.com")
    print("   - Inni: https://core.telegram.org/bots/payments#supported-payment-providers")
    print("=" * 50)
    
    # Uruchomienie bota
    print("\n🚀 Uruchamianie bota...")
    dp.run_polling(bot)
