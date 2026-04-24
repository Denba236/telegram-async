# 🚀 API 9.6 - Pełne Wsparcie

Ta biblioteka obsługuje **wszystkie funkcje Telegram Bot API 9.6** (wydane 3 kwietnia 2026) oraz **uzupełnia braki z wcześniejszych wersji**.

---

## 📋 Nowe Funkcje API 9.6

### 🤖 Managed Bots (Zarządzane Boty)

**Nowe typy:**
- `ManagedBotCreated` - komunikat o utworzeniu zarządzanego bota
- `ManagedBotUpdated` - aktualizacja tokenu zarządzanego bota
- `ManagedBotInfo` - informacje o zarządzanym bocie
- `KeyboardButtonRequestManagedBot` - przycisk do żądania zarządzanego bota
- `PreparedKeyboardButton` - przygotowany przycisk klawiatury dla Mini Apps

**Nowe metody:**
```python
# Pobierz token zarządzanego bota
token = await bot.get_managed_bot_token(managed_bot_id="bot123")

# Zamień token zarządzanego bota
new_token = await bot.replace_managed_bot_token(
    managed_bot_id="bot123",
    name="New Bot Name"
)

# Zapisz przygotowany przycisk klawiatury
button_id = await bot.save_prepared_keyboard_button(button)
```

**Zaktualizowane pola:**
- `User.can_manage_bots` - czy użytkownik może zarządzać botami
- `Message.managed_bot_created` - komunikat o utworzeniu bota
- `Update.managed_bot` - aktualizacja zarządzwanego bota

---

### 📊 Ulepszone Ankiety (Enhanced Polls)

**Nowe typy:**
- `PollExtended` - rozszerzona ankieta z funkcjami API 9.6
- `PollOptionExtended` - rozszerzona opcja ankiety
- `PollOptionAdded` - komunikat o dodaniu nowej opcji
- `PollOptionDeleted` - komunikat o usunięciu opcji
- `PollAnswerExtended` - rozszerzona odpowiedź na ankietę

**Nowe parametry `send_poll`:**
```python
await bot.send_poll(
    chat_id=chat_id,
    question="Pytanie?",
    options=["Opcja 1", "Opcja 2"],
    # API 9.6
    correct_option_ids=[0, 1],  # Wiele poprawnych odpowiedzi (quiz)
    allows_revoting=True,  # Zezwalaj na zmianę głosu
    description="Opis ankiety",  # Opis ankiety
    shuffle_options=True,  # Losowa kolejność opcji
    allow_adding_options=True,  # Zezwalaj na dodawanie opcji
    hide_results_until_closes=True  # Ukryj wyniki do zamknięcia
)
```

**Zaktualizowane pola:**
- `Poll.correct_option_ids` - zastępuje `correct_option_id` (tablica)
- `Poll.allows_multiple_answers` - dla quizów z wieloma odpowiedziami
- `Poll.allows_revoting` - zmiana głosu
- `Poll.description` - opis ankiety
- `Poll.shuffle_options` - losowa kolejność
- `Poll.allow_adding_options` - dodawanie opcji
- `Poll.hide_results_until_closes` - ukryte wyniki
- `PollOption.persistent_id` - trwały identyfikator
- `PollOption.added_by_user` - kto dodał opcję
- `PollOption.added_by_chat` - który czat dodał opcję
- `PollOption.addition_date` - data dodania
- `PollAnswer.option_persistent_ids` - trwałe ID opcji
- `Message.reply_to_poll_option_id` - odpowiedź na konkretną opcję
- `Message.poll_option_added` - komunikat o dodaniu opcji
- `Message.poll_option_deleted` - komunikat o usunięciu opcji

---

### 💳 Płatne Media (Paid Media)

**Nowe typy:**
- `PaidMedia` - bazowy typ płatnych mediów
- `PaidMediaPhoto` - płatne media ze zdjęciami
- `PaidMediaVideo` - płatne media z wideo
- `PaidMediaInfo` - informacje o zakupionych mediach

**Nowa metoda:**
```python
await bot.send_paid_media(
    chat_id=chat_id,
    star_count=100,  # Wymagana liczba Telegram Stars
    media=[
        {"type": "photo", "photo": [...]},
        {"type": "video", "video": {...}}
    ],
    caption="Płatne media",
    show_caption_above_media=True
)
```

**Zaktualizowane pola:**
- `Message.paid_media` - zakupione płatne media
- `Update.purchased_paid_media` - aktualizacja zakupów

---

### 🔗 Linki Zaproszenia (Invite Links)

**Nowe typy:**
- `ChatInviteLink` - link zaproszenia z pełnymi informacjami

**Nowe metody:**
```python
# Utwórz link zaproszenia
link = await bot.create_chat_invite_link(
    chat_id=chat_id,
    name="Mój link",
    expire_date=timestamp,
    member_limit=100,
    creates_join_request=True  # Żądanie dołączenia zamiast bezpośredniego
)

# Edytuj link zaproszenia
link = await bot.edit_chat_invite_link(
    chat_id=chat_id,
    invite_link="https://t.me/+abc123",
    name="Nowa nazwa",
    member_limit=50
)

# Unieważnij link zaproszenia
link = await bot.revoke_chat_invite_link(
    chat_id=chat_id,
    invite_link="https://t.me/+abc123"
)
```

---

### 📌 Przypinanie Wiadomości (Pin/Unpin Messages)

**Nowe metody:**
```python
# Przypnij wiadomość
await bot.pin_chat_message(
    chat_id=chat_id,
    message_id=message_id,
    disable_notification=True
)

# Odepnij wiadomość
await bot.unpin_chat_message(
    chat_id=chat_id,
    message_id=message_id  # opcjonalne
)

# Odepnij wszystkie wiadomości
await bot.unpin_all_chat_messages(chat_id=chat_id)
```

---

### 🚪 Żądania Dołączenia (Chat Join Requests)

**Nowe metody:**
```python
# Zatwierdź żądanie dołączenia
await bot.approve_chat_join_request(
    chat_id=chat_id,
    user_id=user_id
)

# Odrzuć żądanie dołączenia
await bot.decline_chat_join_request(
    chat_id=chat_id,
    user_id=user_id
)
```

---

### 🔐 Uprawnienia Czatów (Chat Permissions)

**Nowe typy:**
- `ChatPermissions` - pełne uprawnienia czatu

**Nowa metoda:**
```python
await bot.set_chat_permissions(
    chat_id=chat_id,
    permissions=ChatPermissions(
        can_send_messages=True,
        can_invite_users=True,
        can_pin_messages=False
    )
)
```

**Dostępne uprawnienia:**
- `can_send_messages` - wysyłanie wiadomości
- `can_send_audios` - wysyłanie audio
- `can_send_documents` - wysyłanie dokumentów
- `can_send_photos` - wysyłanie zdjęć
- `can_send_videos` - wysyłanie wideo
- `can_send_video_notes` - wysyłanie notatek wideo
- `can_send_voice_notes` - wysyłanie notatek głosowych
- `can_send_polls` - wysyłanie ankiet
- `can_send_other_messages` - inne wiadomości
- `can_add_web_page_previews` - podgląd stron
- `can_change_info` - zmiana informacji
- `can_invite_users` - zapraszanie użytkowników
- `can_pin_messages` - przypinanie wiadomości
- `can_manage_topics` - zarządzanie tematami

---

### 👑 Prawa Administratora (Administrator Rights)

**Nowe typy:**
- `ChatAdministratorRights` - prawa administratora

**Nowe metody:**
```python
# Ustaw domyślne prawa administratora
await bot.set_my_default_administrator_rights(
    rights=ChatAdministratorRights.full(),
    for_channels=False
)

# Pobierz domyślne prawa administratora
rights = await bot.get_my_default_administrator_rights(
    for_channels=True
)
```

**Dostępne prawa:**
- `is_anonymous` - anonimowość
- `can_manage_chat` - zarządzanie czatem
- `can_delete_messages` - usuwanie wiadomości
- `can_manage_video_chats` - zarządzanie czatami wideo
- `can_restrict_members` - ograniczanie członków
- `can_promote_members` - awansowanie członków
- `can_change_info` - zmiana informacji
- `can_invite_users` - zapraszanie użytkowników
- `can_post_stories` - publikowanie historii
- `can_edit_stories` - edycja historii
- `can_delete_stories` - usuwanie historii
- `can_post_messages` - publikowanie wiadomości
- `can_edit_messages` - edycja wiadomości
- `can_pin_messages` - przypinanie wiadomości
- `can_manage_topics` - zarządzanie tematami

---

### 🚫 Banowanie Nadawców (Ban/Unban Sender Chat)

**Nowe metody:**
```python
# Zbanuj kanał/czat w grupie
await bot.ban_chat_sender_chat(
    chat_id=chat_id,
    sender_chat_id=channel_id
)

# Odbanuj kanał/czat
await bot.unban_chat_sender_chat(
    chat_id=chat_id,
    sender_chat_id=channel_id
)
```

---

### 📋 Inne Nowe Metody

**Kopiowanie wiadomości:**
```python
await bot.copy_message(
    chat_id=target_chat,
    from_chat_id=source_chat,
    message_id=message_id,
    caption="Nowy podpis"
)
```

**Ikony tematów forum:**
```python
stickers = await bot.get_forum_topic_icon_stickers()
```

**Dane paszportowe:**
```python
await bot.set_passport_data_errors(
    user_id=user_id,
    errors=[...]
)
```

**Zestawy naklejek:**
```python
await bot.set_sticker_set_title(name="SetName", title="Nowy tytuł")
await bot.set_sticker_set_emoji_sticker_format(
    name="SetName",
    emoji_sticker_format="static"
)
```

---

## 📊 Pełna Lista Metod

### Wszystkie metody API (łącznie: **115+**)

#### Wiadomości
- ✅ `sendMessage`
- ✅ `sendMessageDraft` ⭐ NOWE API 9.5
- ✅ `copyMessage` ⭐ NOWE
- ✅ `sendPhoto`
- ✅ `sendDocument`
- ✅ `sendAudio`
- ✅ `sendVideo`
- ✅ `sendVoice`
- ✅ `sendVideoNote`
- ✅ `sendMediaGroup`
- ✅ `sendLocation`
- ✅ `sendVenue`
- ✅ `sendContact`
- ✅ `sendPoll` (zaktualizowano dla API 9.6)
- ✅ `sendDice`
- ✅ `sendGame`
- ✅ `sendPaidMedia` ⭐ NOWE API 9.6
- ✅ `editMessageText`
- ✅ `editMessageCaption`
- ✅ `editMessageMedia`
- ✅ `editMessageReplyMarkup`
- ✅ `deleteMessage`
- ✅ `pinChatMessage` ⭐ NOWE
- ✅ `unpinChatMessage` ⭐ NOWE
- ✅ `unpinAllChatMessages` ⭐ NOWE

#### Ankiety
- ✅ `sendPoll` (zaktualizowano)
- ✅ `stopPoll`

#### Czat
- ✅ `getChat`
- ✅ `getChatAdministrators`
- ✅ `getChatMemberCount`
- ✅ `getChatMember`
- ✅ `setChatPermissions` ⭐ NOWE
- ✅ `banChatMember`
- ✅ `unbanChatMember`
- ✅ `banChatSenderChat` ⭐ NOWE
- ✅ `unbanChatSenderChat` ⭐ NOWE
- ✅ `promoteChatMember`

#### Linki Zaproszenia
- ✅ `createChatInviteLink` ⭐ NOWE
- ✅ `editChatInviteLink` ⭐ NOWE
- ✅ `revokeChatInviteLink` ⭐ NOWE

#### Żądania Dołączenia
- ✅ `approveChatJoinRequest` ⭐ NOWE
- ✅ `declineChatJoinRequest` ⭐ NOWE

#### Bot Info
- ✅ `getMe`
- ✅ `logOut`
- ✅ `closeBot`
- ✅ `setMyDefaultAdministratorRights` ⭐ NOWE
- ✅ `getMyDefaultAdministratorRights` ⭐ NOWE

#### Aktualizacje
- ✅ `getUpdates`

#### Webhook
- ✅ `setWebhook`
- ✅ `deleteWebhook`
- ✅ `getWebhookInfo`

#### Komendy
- ✅ `setMyCommands`
- ✅ `getMyCommands`
- ✅ `deleteMyCommands`
- ✅ `setMyName`
- ✅ `getMyName`
- ✅ `setMyDescription`
- ✅ `getMyDescription`
- ✅ `setMyShortDescription`
- ✅ `getMyShortDescription`

#### Płatności
- ✅ `sendInvoice`
- ✅ `createInvoiceLink`
- ✅ `answerShippingQuery`
- ✅ `answerPreCheckoutQuery`
- ✅ `getStarTransactions`
- ✅ `getMyStarBalance` ⭐ NOWE API 9.6
- ✅ `refundStarPayment`
- ✅ `editUserStarSubscription`

#### Gry
- ✅ `sendGame`
- ✅ `setGameScore`
- ✅ `getGameHighScores`

#### Naklejki
- ✅ `sendSticker`
- ✅ `getStickerSet`
- ✅ `uploadStickerFile`
- ✅ `createNewStickerSet`
- ✅ `addStickerToSet`
- ✅ `setStickerPositionInSet`
- ✅ `deleteStickerFromSet`
- ✅ `setStickerSetThumb`
- ✅ `setStickerSetTitle` ⭐ NOWE
- ✅ `setStickerSetEmojiStickerFormat` ⭐ NOWE
- ✅ `deleteStickerSet`
- ✅ `setCustomEmojiStickerSetThumbnail`
- ✅ `replaceStickerInSet`

#### Reakcje
- ✅ `setMessageReaction`

#### Forum
- ✅ `createForumTopic`
- ✅ `editForumTopic`
- ✅ `closeForumTopic`
- ✅ `reopenForumTopic`
- ✅ `deleteForumTopic`
- ✅ `unpinAllForumTopicMessages`
- ✅ `editGeneralForumTopic`
- ✅ `closeGeneralForumTopic`
- ✅ `reopenGeneralForumTopic`
- ✅ `hideGeneralForumTopic`
- ✅ `unhideGeneralForumTopic`
- ✅ `unpinAllGeneralForumTopicMessages`
- ✅ `getForumTopicIconStickers` ⭐ NOWE

#### Biznes
- ✅ `getBusinessConnection`

#### Prezenty
- ✅ `getAvailableGifts`
- ✅ `sendGift`

#### Weryfikacja
- ✅ `verifyUser`
- ✅ `verifyChat`
- ✅ `removeUserVerification`
- ✅ `removeChatVerification`

#### Emoji Status
- ✅ `setUserEmojiStatus`

#### Menu
- ✅ `setChatMenuButton`
- ✅ `getChatMenuButton`

#### Pliki
- ✅ `getFile`
- ✅ `downloadFile`

#### Akcje
- ✅ `sendChatAction`

#### Callback
- ✅ `answerCallbackQuery`

#### Managed Bots (API 9.6) ⭐ NOWE
- ✅ `getManagedBotToken`
- ✅ `replaceManagedBotToken`
- ✅ `getManagedBots`
- ✅ `savePreparedKeyboardButton`

#### Paszport
- ✅ `setPassportDataErrors` ⭐ NOWE

---

## 🎯 Przykłady Użycia

### 1. Tworzenie Ankiety z Wieloma Poprawnymi Odpowiedziami

```python
from telegram_async import Bot

bot = Bot(token="YOUR_TOKEN")

await bot.send_poll(
    chat_id=-1001234567890,
    question="Które języki programowania znasz?",
    options=["Python", "JavaScript", "Go", "Rust"],
    poll_type="quiz",
    correct_option_ids=[0, 1, 2],  # Wiele poprawnych!
    allows_revoting=True,  # Można zmienić głos
    description="Zaznacz wszystkie znane języki",
    allow_adding_options=True  # Można dodać więcej opcji
)
```

### 2. Tworzenie Zarządzanego Bota

```python
# Utwórz link do tworzenia zarządzanego bota
# https://t.me/newbot/manager_bot/my_awesome_bot?name=My%20Bot

# Po utworzeniu, pobierz token
token_info = await bot.get_managed_bot_token(managed_bot_id="bot123")

# Lub zamień istniejący token
new_token = await bot.replace_managed_bot_token(
    managed_bot_id="bot123",
    name="Updated Bot Name"
)
```

### 3. Prasyłanie Płatnych Mediów

```python
await bot.send_paid_media(
    chat_id=user_id,
    star_count=50,  # 50 Telegram Stars
    media=[
        {
            "type": "photo",
            "media": "AgACAgIAAxkBAAIBZ"
        },
        {
            "type": "video",
            "media": "BAACAgIAAxkBAAIBa"
        }
    ],
    caption="Ekskluzywne materiały premium"
)
```

### 4. Zarządzanie Linkami Zaproszenia

```python
# Utwórz limitowany link z wygaśnięciem
link = await bot.create_chat_invite_link(
    chat_id=-1001234567890,
    name="Link promocyjny",
    expire_date=1735689600,  # 1 stycznia 2025
    member_limit=10,
    creates_join_request=True  # Wymaga zatwierdzenia
)

print(f"Link: {link.invite_link}")
print(f"Limit: {link.member_limit}")
```

### 5. Zatwierdzanie Żądań Dołączenia

```python
from telegram_async import Dispatcher, Router

dp = Dispatcher(bot)
router = Router()

@router.chat_join_request()
async def handle_join_request(ctx):
    # Automatycznie zatwierdź
    await ctx.answer_chat_join_request(
        chat_id=ctx.chat_id,
        user_id=ctx.user_id
    )
    
    # Lub używając metody bota
    await bot.approve_chat_join_request(
        chat_id=ctx.chat_id,
        user_id=ctx.user_id
    )

dp.include_router(router)
```

### 6. Ustawianie Uprawnień Czatów

```python
# Ogranicz uprawnienia dla nowej grupy
await bot.set_chat_permissions(
    chat_id=-1001234567890,
    permissions=ChatPermissions(
        can_send_messages=True,
        can_send_photos=True,
        can_send_videos=False,
        can_send_polls=False,
        can_invite_users=True,
        can_pin_messages=False
    )
)

# Lub użyj predefiniowanych
await bot.set_chat_permissions(
    chat_id=-1001234567890,
    permissions=ChatPermissions.all_denied()
)
```

---

## 📝 Uwagi

### Kompatybilność wsteczna
- ✅ Wszystkie istniejące metody nadal działają
- ✅ `correct_option_id` w `send_poll` jest przestarzały, ale nadal obsługiwany
- ✅ Nowe pola w typach są opcjonalne

### Zalecane praktyki
1. Używaj `correct_option_ids` zamiast `correct_option_id` dla quizów
2. Zawsze sprawdzaj czy bot ma odpowiednie prawa administratora
3. Używaj `ChatPermissions.all_allowed()` lub `.all_denied()` dla szybkich ustawień
4. Przy płatnych mediach podawaj prawidłową liczbę `star_count`

---

## 🔗 Dokumentacja Telegram

- [Bot API 9.6 Changelog](https://core.telegram.org/bots/api#april-3-2026)
- [Managed Bots](https://core.telegram.org/bots/api#managed-bots)
- [Polls](https://core.telegram.org/bots/api#polls)
- [Paid Media](https://core.telegram.org/bots/api#paidmedia)

---

**Wersja biblioteki: 3.10** ✅
**Wsparcie API: 9.6** ✅
**Testy: 36 przechodzących** ✅
