# 🌟 Bot Telegram Premium - Dokumentacja

## ⚠️ WAŻNE ZANIM ZACZNIESZ

### Bot NIE aktywuje Premium automatycznie!

Telegram Premium **NIE MOŻE** być aktywowany przez bota. Bot może jedynie:
- ✅ Przyjąć płatność w Telegram Stars
- ✅ Dać instrukcję jak aktywować Premium
- ✅ Zapisać transakcję w bazie danych

**Użytkownik musi ręcznie aktywować Premium** w ustawieniach Telegrama.

---

## 💡 Jak to działa?

### Proces:

```
1. Użytkownik klika /premium
   ↓
2. Bot wysyła fakturę (250 Stars)
   ↓
3. Użytkownik płaci Stars
   ↓
4. Bot potwierdza płatność
   ↓
5. Bot daje instrukcję aktywacji
   ↓
6. Użytkownik aktywuje Premium w Telegram Settings
   ↓
7. Premium aktywowany! ✅
```

---

## 🚀 Uruchomienie

### 1. Konfiguracja

```python
# examples/premium_bot.py
BOT_TOKEN = "YOUR_BOT_TOKEN"  # Zmień na swój token
PREMIUM_STARS = 250  # Cena za 1 miesiąc
```

### 2. Uzyskaj Bot Token

1. Otwórz [@BotFather](https://t.me/botfather)
2. Wyślij: `/newbot`
3. Podaj nazwę i username
4. Skopiuj token

### 3. Uruchom bota

```bash
cd examples
python premium_bot.py
```

---

## 💰 Cennik Premium

### Aktualne ceny (w Stars):

| Okres | Stars | USD (ok.) | PLN (ok.) |
|-------|-------|-----------|-----------|
| **1 miesiąc** | 250 ⭐ | $3.25 | ~13 PLN |
| 3 miesiące | 700 ⭐ | $9.10 | ~36 PLN |
| 6 miesięcy | 1300 ⭐ | $16.90 | ~68 PLN |
| 12 miesięcy | 2500 ⭐ | $32.50 | ~130 PLN |

⚠️ **Ceny mogą się zmieniać** - sprawdź w Telegram Settings → Premium

---

## 📝 Przykłady Użycia

### Podstawowy bot (gotowy!)

Plik: `examples/premium_bot.py`

```python
from telegram_async import Bot, Dispatcher, Router
from telegram_async.telegram_types.new_types import LabeledPrice

BOT_TOKEN = "YOUR_BOT_TOKEN"
PREMIUM_STARS = 250

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
router = Router()

@router.command("premium")
async def cmd_premium(ctx):
    await ctx.send_invoice(
        title="🌟 Telegram Premium (1 miesiąc)",
        description="Aktywacja Premium na 30 dni",
        payload=f"premium_{ctx.user_id}",
        provider_token="",  # Puste dla Stars
        currency="XTR",
        prices=[
            LabeledPrice(label="Premium - 1 miesiąc", amount=PREMIUM_STARS)
        ]
    )

@router.pre_checkout_query()
async def pre_checkout(ctx):
    await ctx.answer_pre_checkout_query(ok=True)

@router.successful_payment()
async def success(ctx):
    stars = ctx.successful_payment.total_amount
    await ctx.reply(
        f"✅ Zapłacono {stars} Stars!\n\n"
        f"Aktywuj Premium w:\n"
        f"Ustawienia → Telegram Premium"
    )

dp.include_router(router)
dp.run_polling(bot)
```

---

## 🎨 Customizacja

### 1. Zmień cenę

```python
# Cena za 1 miesiąc
PREMIUM_STARS = 300  # Zmień na inną kwotę
```

### 2. Dodaj zniżkę za dłuższy okres

```python
PRICES = {
    "1month": {"stars": 250, "days": 30},
    "3months": {"stars": 700, "days": 90},  # Oszczędzasz 50 Stars
    "6months": {"stars": 1300, "days": 180},  # Oszczędzasz 200 Stars
}

@router.command("premium")
async def cmd_premium(ctx):
    # Wyślij menu z opcjami
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("1 miesiąc - 250 ⭐", callback_data="premium_1m"))
    keyboard.add(InlineKeyboardButton("3 miesiące - 700 ⭐", callback_data="premium_3m"))
    keyboard.add(InlineKeyboardButton("6 miesięcy - 1300 ⭐", callback_data="premium_6m"))
    
    await ctx.reply("Wybierz okres Premium:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("premium_"))
async def handle_premium_select(ctx):
    period = ctx.callback_query.data
    
    if period == "premium_1m":
        stars = 250
        days = 30
    elif period == "premium_3m":
        stars = 700
        days = 90
    elif period == "premium_6m":
        stars = 1300
        days = 180
    
    await ctx.send_invoice(
        title=f"🌟 Premium ({days} dni)",
        description=f"Telegram Premium na {days} dni",
        payload=f"premium_{period}_{ctx.user_id}",
        currency="XTR",
        prices=[LabeledPrice(label=f"Premium ({days} dni)", amount=stars)]
    )
```

### 3. Dodaj bazę danych

```python
# Dodaj do successful_payment handler
import sqlite3
from datetime import datetime, timedelta

async def save_premium_to_db(user_id: int, stars: int, days: int):
    """Zapisz aktywację Premium do bazy danych"""
    conn = sqlite3.connect('premium.db')
    cursor = conn.cursor()
    
    # Utwórz tabelę jeśli nie istnieje
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS premium_users (
            user_id INTEGER PRIMARY KEY,
            stars_paid INTEGER,
            activated_at TIMESTAMP,
            expires_at TIMESTAMP
        )
    ''')
    
    # Wstaw dane
    now = datetime.now()
    expires = now + timedelta(days=days)
    
    cursor.execute('''
        INSERT OR REPLACE INTO premium_users 
        (user_id, stars_paid, activated_at, expires_at)
        VALUES (?, ?, ?, ?)
    ''', (user_id, stars, now, expires))
    
    conn.commit()
    conn.close()

@router.successful_payment()
async def success(ctx):
    stars = ctx.successful_payment.total_amount
    
    # Zapisz do bazy
    await save_premium_to_db(
        user_id=ctx.user_id,
        stars=stars,
        days=30
    )
    
    await ctx.reply("✅ Premium aktywowany!")
```

### 4. Sprawdź czy użytkownik ma Premium

```python
@router.command("status")
async def check_status(ctx):
    """Sprawdź status Premium użytkownika"""
    # Sprawdź w bazie danych
    conn = sqlite3.connect('premium.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT expires_at FROM premium_users WHERE user_id = ?',
        (ctx.user_id,)
    )
    result = cursor.fetchone()
    conn.close()
    
    if result:
        expires = datetime.fromisoformat(result[0])
        if expires > datetime.now():
            days_left = (expires - datetime.now()).days
            await ctx.reply(
                f"✅ <b>Masz aktywne Premium!</b>\n\n"
                f"📅 Wygasa za: {days_left} dni\n"
                f"📆 Data wygaśnięcia: {expires.strftime('%d.%m.%Y')}"
            )
        else:
            await ctx.reply(
                "❌ <b>Premium wygasł</b>\n\n"
                "Użyj /premium aby odnowić"
            )
    else:
        await ctx.reply(
            "❌ <b>Nie masz Premium</b>\n\n"
            "Użyj /premium aby kupić"
        )
```

---

## 💵 Jak zarabiasz?

### Proces wypłaty:

1. **Użytkownicy płacą Stars** w Twoim bocie
2. **Stars gromadzą się** na koncie bota
3. **Wymieniasz Stars na pieniądze** przez @BotFather
4. **Pieniądze trafiają** na Twoje konto bankowe

### Ile zarobisz?

| Premium sprzedane | Stars zebrane | Prowizja (30%) | Otrzymasz |
|-------------------|---------------|----------------|-----------|
| 10 użytkowników | 2500 | -750 | ~$22.75 |
| 50 użytkowników | 12500 | -3750 | ~$113.75 |
| 100 użytkowników | 25000 | -7500 | ~$227.50 |
| 500 użytkowników | 125000 | -37500 | ~$1137.50 |

**Przykład:**
```
100 użytkowników × 250 Stars = 25000 Stars
Wartość: ~$325
Prowizja Telegrama (30%): -$97.50
Otrzymasz: ~$227.50
```

---

## 📊 Statystyki

### Sprawdź ile Stars zebrano:

1. Otwórz [@BotFather](https://t.me/botfather)
2. Wyślij: `/mybots`
3. Wybierz bota
4. Kliknij: `Statistics`
5. Zobaczysz:
   - ⭐ Zebrane Stars
   - 💵 Kwota do wypłaty
   - 📊 Statystyki użytkowników

### Wypłać pieniądze:

1. @BotFather → `/mybots` → Bot
2. Kliknij: `Payments`
3. Kliknij: `Withdraw`
4. Podaj dane konta bankowego
5. Czekaj 1-3 dni na przelew

---

## ❓ FAQ

### P: Czy bot aktywuje Premium automatycznie?
O: **NIE**. Użytkownik musi aktywować ręcznie w Ustawieniach → Telegram Premium.

### P: Dlaczego nie automatycznie?
O: Telegram nie pozwala botom na bezpośrednią aktywację Premium. To ograniczenie API.

### P: Jak użytkownik aktywuje Premium?
O: 
1. Ustawienia Telegram
2. Kliknij "Telegram Premium"
3. Kliknij "Activate" lub "Aktywuj"
4. Gotowe!

### P: Ile kosztuje Premium?
O: Około 250 Stars za miesiąc (~$3.25 / ~13 PLN).

### P: Czy mogę zmienić cenę?
O: Tak, zmień `PREMIUM_STARS` w kodzie bota.

### P: Co jeśli użytkownik nie aktywuje?
O: Stars i tak trafiają na konto bota. Użytkownik może aktywować kiedy chce.

### P: Czy mogę sprzedawać na dłuższy okres?
O: Tak! Zmień opis i dostosuj liczbę Stars.

---

## ⚖️ Uwagi Prawne

### ⚠️ Ważne:

1. **Nie obiecuj automatycznej aktywacji** - to niemożliwe
2. **Poinformuj użytkowników** że muszą aktywować ręcznie
3. **Zachowaj dowody transakcji** - ID płatności z Telegram
4. **Bądź transparentny** - pokaż ile kosztuje Premium

### ✅ Dobre praktyki:

- Wyraźnie napisz że aktywacja jest ręczna
- Podaj instrukcję krok po kroku
- Zachowaj ID transakcji w bazie danych
- Odpowiadaj na pytania użytkowników

---

## 🔗 Przydatne Linki

- [Telegram Premium](https://telegram.org/premium)
- [Telegram Stars Documentation](https://core.telegram.org/bots/api#stars)
- [BotFather](https://t.me/botfather)
- [Cennik Premium](https://telegram.org/blog/premium)

---

## 📞 Pomoc

Masz pytania? Napisz do nas:
- 📧 Email: ostrovskyidenys30@gmail.com
- 💬 GitHub: https://github.com/Denba236

---

**Gotowe! 🎉 Twój bot Premium jest gotowy do działania!** ⭐
