# 💳 Konfiguracja Płatności w Telegram Bot

## 📋 Wymagania

1. **Bot Token** - uzyskasz u [@BotFather](https://t.me/botfather)
2. **Provider Token** - token dostawcy płatności

## 🔧 Krok 1: Wybór Dostawcy Płatności

Telegram obsługuje wielu dostawców płatności:

### Stripe (Rekomendowane)
- 🌐 Strona: https://stripe.com
- ✅ Obsługuje PLN (złotówki)
- ✅ Łatwa konfiguracja
- ✅ Niskie prowizje (1.4% + 1.00 PLN)

#### Jak uzyskać Provider Token (Stripe):

1. **Załóż konto na Stripe**
   - Wejdź na https://stripe.com
   - Kliknij "Sign up"
   - Wypełnij formularz

2. **Aktywuj tryb testowy** (do testów)
   - W panelu Stripe przełącz na "Test mode"
   - Skopiuj klucz API z sekcji "Developers → API keys"

3. **Podłącz Stripe do Telegrama**
   - Otwórz [@BotFather](https://t.me/botfather)
   - Wyślij `/mybots`
   - Wybierz swojego bota
   - Kliknij `Bot Settings` → `Payments`
   - Wybierz `Stripe`
   - Wklej klucz API ze Stripe
   - BotFather wygeneruje **Provider Token**

4. **Skopiuj Provider Token**
   - Po skonfigurowaniu, BotFather pokaże Provider Token
   - Wklej go do pliku bota w zmienną `PROVIDER_TOKEN`

### Inni Dostawcy
- **YooMoney** - dla Rosji
- **Payme** - dla Uzbekistanu
- **Click** - dla Uzbekistanu
- **Tranzzo** - międzynarodowy

Pełna lista: https://core.telegram.org/bots/payments#supported-payment-providers

---

## 💻 Krok 2: Uruchomienie Bota

### Opcja 1: Prosty Bot (5 PLN)

```python
# examples/payment_simple_bot.py
from telegram_async import Bot, Dispatcher, Router

BOT_TOKEN = "TWÓJ_BOT_TOKEN"
PROVIDER_TOKEN = "TWÓJ_PROVIDER_TOKEN"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
router = Router()

@router.command("pay")
async def cmd_pay(ctx):
    await ctx.answer(
        title="Płatność 5 PLN",
        description="Opłata za usługę",
        payload="payment_5pln",
        provider_token=PROVIDER_TOKEN,
        currency="PLN",
        prices=[{"label": "Usługa", "amount": 500}]  # 5 PLN w groszach
    )

@router.pre_checkout_query()
async def pre_checkout(ctx):
    await ctx.answer_pre_checkout_query(ok=True)

@router.successful_payment()
async def success(ctx):
    amount = ctx.successful_payment.total_amount / 100
    await ctx.reply(f"✅ Zapłacono {amount} PLN. Dziękujemy!")

dp.include_router(router)
dp.run_polling(bot)
```

### Opcja 2: Pełny Bot Premium

```bash
python examples/payment_bot.py
```

Ten bot zawiera:
- ✅ Stronę startową z cennikiem
- ✅ Fakturę 5 PLN
- ✅ Obsługę udanych płatności
- ✅ Sprawdzanie statusu
- ✅ Pomoc

---

## 🧪 Krok 3: Testowanie Płatności

### Tryb Testowy (Stripe)

1. Użyj **testowych kart kredytowych**:

| Karta | Numer | Opis |
|-------|-------|------|
| ✅ Sukces | `4242 4242 4242 4242` | Płatność przechodzi |
| ❌ Odrzucona | `4000 0000 0000 0002` | Płatność odrzucona |
| ⏸ Wymaga 3D | `4000 0000 0000 3220` | Wymaga autoryzacji 3D Secure |

2. **Dane karty testowej:**
   - Numer: `4242 4242 4242 4242`
   - Data ważności: Dowolna przyszła data (np. `12/25`)
   - CVC: Dowolne 3 cyfry (np. `123`)
   - Imię: Dowolne
   - Email: email@example.com

3. **Proces testowania:**
   ```
   Użytkownik: /pay
   Bot: [Wysyła fakturę]
   Użytkownik: Klika "Zapłać"
   → Wprowadza testową kartę
   → Płatność przechodzi
   Bot: "✅ Płatność zakończona sukcesem!"
   ```

### Tryb Produkcyjny

Gdy gotowy do prawdziwych płatności:

1. W Stripe przełącz na **Live mode**
2. Skopiuj **Live API Key**
3. Zaktualizuj `PROVIDER_TOKEN` w bocie
4. Gotowe! 🎉

---

## 💡 Jak Działają Płatności?

### Proces Płatności:

```
1. Użytkownik klika /pay
   ↓
2. Bot wysyła fakturę (Invoice)
   ↓
3. Użytkownik klika "Zapłać"
   ↓
4. pre_checkout_query() - walidacja
   ↓
5. Użytkownik potwierdza płatność
   ↓
6. Telegram przetwarza płatność
   ↓
7. successful_payment() - potwierdzenie
   ↓
8. Bot aktywuje usługę premium
```

### Struktura Ceny:

```python
# Kwota jest w GROSZACH (najmniejsza jednostka waluty)
5 PLN = 500 groszy
10 PLN = 1000 groszy
50 PLN = 5000 groszy

prices = [
    {"label": "Nazwa usługi", "amount": 500}  # 5 PLN
]
```

---

## 🎨 Przykłady Użycia

### 1. Jednorazowa Płatność

```python
@router.command("buy")
async def cmd_buy(ctx):
    await ctx.answer(
        title="Kup Przedmiot",
        description="Magiczny miecz +10 do ataku",
        payload="sword_001",
        provider_token=PROVIDER_TOKEN,
        currency="PLN",
        prices=[{"label": "Magiczny Miecz", "amount": 5000}]  # 50 PLN
    )
```

### 2. Subskrypcja Miesięczna

```python
@router.command("subscribe")
async def cmd_subscribe(ctx):
    await ctx.answer(
        title="Subskrypcja Premium",
        description="Dostęp premium na 30 dni",
        payload=f"sub_{ctx.user_id}_{int(time.time())}",
        provider_token=PROVIDER_TOKEN,
        currency="PLN",
        prices=[{"label": "Premium (miesiąc)", "amount": 500}],
        need_email=True
    )
```

### 3. Donacje/Tipy

```python
@router.command("donate")
async def cmd_donate(ctx):
    amount = 500  # 5 PLN
    
    await ctx.answer(
        title="Wesprzyj Nas",
        description="Dowolna kwota na rozwój bota",
        payload=f"donate_{ctx.user_id}",
        provider_token=PROVIDER_TOKEN,
        currency="PLN",
        prices=[{"label": "Wsparcie", "amount": amount}],
        is_flexible=True  # Pozwala na zmianę kwoty
    )
```

### 4. Płatność z Danymi Wysyłki

```python
@router.command("order")
async def cmd_order(ctx):
    await ctx.answer(
        title="Zamówienie",
        description="Fizyczny produkt z wysyłką",
        payload=f"order_{ctx.user_id}",
        provider_token=PROVIDER_TOKEN,
        currency="PLN",
        prices=[
            {"label": "Produkt", "amount": 5000},
            {"label": "Wysyłka", "amount": 1000}
        ],
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True
    )
```

---

## 🔐 Bezpieczeństwo

### ✅ Dobre Praktyki:

1. **Waliduj płatności:**
   ```python
   @router.pre_checkout_query()
   async def pre_checkout(ctx):
       # Sprawdź czy payload jest poprawny
       if not ctx.invoice_payload.startswith("payment_"):
           await ctx.answer_pre_checkout_query(
               ok=False,
               error_message="Nieprawidłowa płatność"
           )
           return
       
       # Zaakceptuj
       await ctx.answer_pre_checkout_query(ok=True)
   ```

2. **Zapisuj transakcje:**
   ```python
   @router.successful_payment()
   async def success(ctx):
       payment = ctx.successful_payment
       
       # Zapisz do bazy danych
       await db.save({
           "user_id": ctx.user_id,
           "amount": payment.total_amount,
           "currency": payment.currency,
           "telegram_id": payment.telegram_payment_charge_id,
           "provider_id": payment.provider_payment_charge_id,
           "date": datetime.now()
       })
   ```

3. **Unikaj duplikatów:**
   ```python
   @router.successful_payment()
   async def success(ctx):
       # Sprawdź czy płatność już nie została zpracowana
       if await db.payment_exists(ctx.successful_payment.telegram_payment_charge_id):
           return
       
       # Przetwórz płatność
       await process_payment(ctx)
   ```

---

## ❓ FAQ

### P: Czy muszę mieć firmę żeby przyjmować płatności?
O: Do testów nie. Do prawdziwych płatności zależy od dostawcy (Stripe wymaga danych firmy).

### P: Ile kosztuje przyjmowanie płatności?
O: Stripe pobiera ~1.4% + 1.00 PLN za transakcję. Dla 5 PLN to ok. 1.07 PLN prowizji.

### P: Czy mogę przyjmować dotacje?
O: Tak! Użyj komendy `/donate` z dowolną kwotą.

### P: Jak zwrócić pieniądze?
O: W panelu Stripe znajdź transakcję i kliknij "Refund".

### P: Czy mogę zmienić kwotę po wysłaniu faktury?
O: Nie. Musisz wysłać nową fakturę z poprawioną kwotą.

---

## 🔗 Przydatne Linki

- [Telegram Payments Docs](https://core.telegram.org/bots/api#payments)
- [Stripe Dashboard](https://dashboard.stripe.com)
- [BotFather](https://t.me/botfather)
- [Test Cards](https://stripe.com/docs/testing#cards)

---

## 📞 Pomoc

Masz pytania? Napisz do nas:
- 📧 Email: ostrovskyidenys30@gmail.com
- 💬 GitHub: https://github.com/Denba236

---

**Gotowe! 🎉 Twój bot jest gotowy do przyjmowania płatności!**
