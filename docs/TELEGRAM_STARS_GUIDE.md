# ⭐ Telegram Stars - Kompletny Przewodnik

## 🌟 Co to są Telegram Stars?

**Telegram Stars** to wewnętrzna waluta Telegrama wprowadzona w **API 9.5** (2024).

### Jak to działa?

```
Użytkownik:
1. Kupuje Stars w Telegram (Ustawienia → Telegram Stars)
2. Płaci w bocie Stars zamiast kartą
3. Bot otrzymuje Stars
4. Bot wymienia Stars na pieniądze
```

---

## 💰 Zalety Telegram Stars

### ✅ Dla Użytkownika:
- 🚀 **Szybkie płatności** - bez podawania karty
- 🔒 **Bezpieczne** - płatność przez Telegram
- 💳 **Jedno miejsce** - wszystkie płatności w Telegram
- 🌍 **Globalne** - działa we wszystkich krajach

### ✅ Dla Developera:
- ✨ **Brak provider_token!** - nie potrzebujesz Stripe
- 🎯 **Prosta integracja** - wystarczy Bot Token
- 💵 **Wypłata pieniędzy** - wymień Stars na pieniądze
- 🌐 **Dostępne wszędzie** - nie zależy od kraju

---

## 🚀 Jak Stworzyć Bota z Stars?

### Krok 1: Token Bota

1. Otwórz **[@BotFather](https://t.me/botfather)**
2. Wyślij: `/newbot`
3. Podaj nazwę i username
4. Skopiuj **BOT_TOKEN**

### Krok 2: Ustaw walutę na XTR

```python
CURRENCY = "XTR"  # Telegram Stars
STARS_AMOUNT = 5  # 5 Stars
```

### Krok 3: Wyślij fakturę

```python
await ctx.answer(
    title="⭐ 5 Telegram Stars",
    description="Płatność za usługę",
    payload="stars_payment_5",
    currency="XTR",  # ⭐ To jest kluczowe!
    prices=[
        {"label": "5 Stars", "amount": 5}  # W Stars, NIE w groszach!
    ]
)
```

### ⚠️ WAŻNE:

| Cecha | Zwykłe płatności | Telegram Stars |
|-------|------------------|----------------|
| **Waluta** | PLN, USD, EUR | **XTR** |
| **provider_token** | ✅ Wymagany | ❌ **NIE MA!** |
| **amount** | W groszach (500 = 5 PLN) | **W Stars** (5 = 5 Stars) |
| **Dostawca** | Stripe, YooMoney | **Brak - przez Telegram** |

---

## 📝 Pełny Przykład

```python
from telegram_async import Bot, Dispatcher, Router
from telegram_async.telegram_types.new_types import LabeledPrice

BOT_TOKEN = "YOUR_BOT_TOKEN"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
router = Router()

@router.command("pay")
async def cmd_pay(ctx):
    await ctx.answer(
        title="⭐ 5 Telegram Stars",
        description="Płatność za usługę premium",
        payload=f"stars_{ctx.user_id}",
        currency="XTR",  # Telegram Stars!
        prices=[
            LabeledPrice(label="5 Stars", amount=5)
        ]
    )

@router.pre_checkout_query()
async def pre_checkout(ctx):
    await ctx.answer_pre_checkout_query(ok=True)

@router.successful_payment()
async def success(ctx):
    stars = ctx.successful_payment.total_amount
    await ctx.reply(
        f"✅ Zapłacono {stars} Stars! Dziękujemy! ⭐"
    )

dp.include_router(router)
dp.run_polling(bot)
```

---

## 💵 Jak Wypłacić Pieniądze z Stars?

### Proces:

```
1. Użytkownicy płacą Stars w Twoim bocie
   ↓
2. Stars gromadzą się na koncie bota
   ↓
3. Wymieniasz Stars na pieniądze
   ↓
4. Pieniądze trafiają na Twoje konto
```

### Krok po kroku:

#### 1. Sprawdź баланс Stars

W **@BotFather**:
```
/mybots → Wybierz bota → Statistics
```

Pokazuje:
- ⭐ Ile Stars zebrano
- 💵 Ile można wypłacić

#### 2. Wypłać pieniądze

W **@BotFather**:
```
/mybots → Wybierz bota → Payments → Withdraw
```

#### 3. Podaj dane do wypłaty

- 🏦 **Konto bankowe** (IBAN)
- 💳 **Lub konto w Stripe** (jeśli masz)
- 📧 **Email** do potwierdzenia

#### 4. Czekaj na przelew

- ⏱ Czas realizacji: **1-3 dni**
- 💰 Kwota: Stars × wartość - prowizja

---

## 💰 Ile Wartość 1 Star?

### Przybliżone wartości:

| Stars | USD (ok.) | PLN (ok.) |
|-------|-----------|-----------|
| 1 ⭐ | $0.013 | 0.05 zł |
| 5 ⭐ | $0.065 | 0.25 zł |
| 50 ⭐ | $0.65 | 2.60 zł |
| 100 ⭐ | $1.30 | 5.20 zł |
| 500 ⭐ | $6.50 | 26 zł |
| 1000 ⭐ | $13.00 | 52 zł |

⚠️ **Wartość może się zmieniać** - sprawdź aktualny kurs w @BotFather

### Prowizja Telegrama:

- Telegram pobiera **ok. 30%** przy wymianie
- Developer otrzymuje **ok. 70%** wartości

**Przykład:**
```
Zebrano: 1000 Stars (≈ $13.00)
Prowizja: -$3.90 (30%)
Otrzymasz: ≈ $9.10
```

---

## 🎯 Przykłady Użycia

### 1. Jednorazowa Płatność

```python
@router.command("buy")
async def cmd_buy(ctx):
    await ctx.answer(
        title="⭐ Kup Przedmiot",
        description="Magiczny miecz +10",
        payload="sword_001",
        currency="XTR",
        prices=[{"label": "Magiczny Miecz", "amount": 50}]  # 50 Stars
    )
```

### 2. Subskrypcja

```python
@router.command("subscribe")
async def cmd_subscribe(ctx):
    await ctx.answer(
        title="⭐ Subskrypcja Premium",
        description="Dostęp na 30 dni",
        payload=f"sub_{ctx.user_id}",
        currency="XTR",
        prices=[{"label": "Premium (miesiąc)", "amount": 100}]  # 100 Stars
    )
```

### 3. Donacje

```python
@router.command("donate")
async def cmd_donate(ctx):
    await ctx.answer(
        title="⭐ Wesprzyj Nas",
        description="Dowolna kwota w Stars",
        payload=f"donate_{ctx.user_id}",
        currency="XTR",
        prices=[{"label": "Wsparcie", "amount": 10}]  # 10 Stars
    )
```

### 4. Wiele Produktów

```python
PRODUCTS = {
    "basic": {"name": "Basic", "stars": 10},
    "premium": {"name": "Premium", "stars": 50},
    "ultimate": {"name": "Ultimate", "stars": 100}
}

@router.command("shop")
async def cmd_shop(ctx):
    text = "🛒 <b>Sklep - Produkty:</b>\n\n"
    for key, prod in PRODUCTS.items():
        text += f"• {prod['name']}: {prod['stars']} Stars ⭐\n"
    text += "\nUżyj /buy <produkt> aby kupić"
    
    await ctx.reply(text, parse_mode="HTML")

@router.command("buy")
async def cmd_buy(ctx, args):
    product_name = args[0] if args else None
    
    if product_name not in PRODUCTS:
        await ctx.reply("❌ Nieznany produkt. Użyj /shop")
        return
    
    product = PRODUCTS[product_name]
    
    await ctx.answer(
        title=f"⭐ {product['name']}",
        description=f"Kupujesz: {product['name']}",
        payload=f"buy_{product_name}_{ctx.user_id}",
        currency="XTR",
        prices=[{"label": product['name'], "amount": product['stars']}]
    )
```

---

## 🆚 Stars vs Zwykłe Płatności

### Telegram Stars ⭐

**Zalety:**
- ✅ Brak provider_token
- ✅ Prosta integracja
- ✅ Działa we wszystkich krajach
- ✅ Szybkie płatności
- ✅ Bezpieczne

**Wady:**
- ❌ Telegram pobiera 30% prowizji
- ❌ Użytkownik musi kupićć Stars
- ❌ Ograniczona wypłata (tylko niektóre kraje)

### Zwykłe Płatności (Stripe)

**Zalety:**
- ✅ Niższa prowizja (ok. 3%)
- ✅ Bezpośrednia wypłata
- ✅ Użytkownik płaci kartą

**Wady:**
- ❌ Wymaga provider_token
- ❌ Stripe nie działa we wszystkich krajach
- ❌ Użytkownik musi podać kartę

---

## 📊 Kiedy Użyć Stars?

### ✅ Tak - Użyj Stars gdy:
- Bot dla użytkowników z różnych krajów
- Nie masz dostępu do Stripe
- Chcesz szybką integrację
- Mniejsze kwoty (< 50 PLN)
- Produkty cyfrowe wewnątrz Telegrama

### ❌ Nie - Użyj Stripe gdy:
- Duże kwoty (> 100 PLN)
- Fizyczne produkty
- Subskrypcje z automatycznym odnawianiem
- Masz dostęp do Stripe
- Niższa prowizja jest ważna

---

## ❓ FAQ

### P: Czy muszę mieć firmę?
O: Do testów nie. Do wypłaty zależy od kraju - sprawdź w @BotFather.

### P: Jak sprawdzić ile Stars zebrałem?
O: @BotFather → /mybots → Bot → Statistics

### P: Jak wypłacić pieniądze?
O: @BotFather → /mybots → Bot → Payments → Withdraw

### P: Ile czasu trwa wypłata?
O: 1-3 dni robocze.

### P: Czy mogę wymieniać Stars na inną walutę?
O: Nie - Stars wymieniają się na USD, potem przeliczają na Twoją walutę.

### P: Co jeśli użytkownik zrefunduje płatność?
O: Stars wracają do użytkownika, Ty tracisz Stars.

---

## 🔗 Przydatne Linki

- [Telegram Stars Documentation](https://core.telegram.org/bots/api#stars)
- [BotFather](https://t.me/botfather)
- [Telegram Blog - Stars](https://telegram.org/blog/stars)

---

## 📞 Pomoc

Masz pytania? Napisz do nas:
- 📧 Email: ostrovskyidenys30@gmail.com
- 💬 GitHub: https://github.com/Denba236

---

**Gotowe! 🎉 Twój bot jest gotowy do przyjmowania Telegram Stars!** ⭐
