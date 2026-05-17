"""
Przykłady użycia nowych funkcji Telegram Bot API 9.5

Nowości w API 9.5:
1. sendMessageDraft - strumieniowe wysyłanie wiadomości
2. setChatMemberTag - zarządzanie tagami członków
3. can_manage_tags - nowe uprawnienie administratora
4. sender_tag - tag nadawcy wiadomości
5. icon_custom_emoji_id - custom emoji dla przycisków
"""

import asyncio
from telegram_async import Bot, Dispatcher, Context
from telegram_async.dispatcher.router import Router
from telegram_async.keyboards import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_async.keyboards import ReplyKeyboardMarkup, ReplyKeyboardButton

bot = Bot("")
dp = Dispatcher()
router = Router(name="api95_examples")

# =====================================================
# 1. sendMessageDraft - Strumieniowe wysyłanie wiadomości
# =====================================================
# Nowa metoda API 9.5 pozwalająca na streamowanie częściowej treści
# wiadomości podczas jej generowania. Tworzy natywny wskaźnik "pisania"
# i dynamicznie aktualizuje tekst.

@router.command("stream")
async def stream_message_example(ctx: Context):
    """Przykład użycia sendMessageDraft do streamowania wiadomości"""
    
    # Przykład 1: Podstawowe użycie sendMessageDraft
    await ctx.client.send_message_draft(
        chat_id=ctx.chat_id,
        text="Generowanie odpowiedzi...",
        streaming_mode="partial"  # 'partial', 'block', lub 'progress'
    )
    
    # Symulacja generowania tekstu
    await asyncio.sleep(1)
    await ctx.client.send_message_draft(
        chat_id=ctx.chat_id,
        text="Generowanie odpowiedzi... Gotowe! ✅",
        streaming_mode="partial"
    )
    
    await asyncio.sleep(1)
    # Finalna wiadomość
    await ctx.reply("Odpowiedź wygenerowana!")


@router.command("stream_progress")
async def progress_stream_example(ctx: Context):
    """Przykład z progress streaming mode"""
    
    # Tryb progress - pokazuje pasek postępu
    for i in range(0, 101, 25):
        await ctx.client.send_message_draft(
            chat_id=ctx.chat_id,
            text=f"Przetwarzanie: {i}%",
            streaming_mode="progress"
        )
        await asyncio.sleep(0.5)
    
    await ctx.reply("Zakończono! 🎉")


# =====================================================
# 2. setChatMemberTag - Zarządzanie tagami członków
# =====================================================
# API 9.5 pozwala ustawiać tagi dla członków grup
# Bot musi mieć uprawnienie can_manage_tags

@router.command("set_tag")
async def set_member_tag(ctx: Context):
    """Przykład ustawiania tagu dla użytkownika"""
    
    # Potrzebujemy user_id i chat_id
    user_id = ctx.user_id
    chat_id = ctx.chat_id
    
    # Ustaw tag dla użytkownika
    success = await ctx.client.set_chat_member_tag(
        chat_id=chat_id,
        user_id=user_id,
        tag="vip_member"  # 0-16 znaków, bez emoji
    )
    
    if success:
        await ctx.reply("✅ Tag ustawiony pomyślnie!")
    else:
        await ctx.reply("❌ Nie udało się ustawić tagu")


@router.command("set_admin_tag")
async def set_custom_tag(ctx: Context):
    """Przykład z custom tagiem"""
    
    # Różne przykłady tagów
    tags = ["moderator", "helper", "vip", "newbie"]
    
    for tag in tags:
        # Możesz ustawić różne tagi dla różnych użytkowników
        await ctx.client.set_chat_member_tag(
            chat_id=ctx.chat_id,
            user_id=ctx.user_id,
            tag=tag
        )
        await asyncio.sleep(0.5)
    
    await ctx.reply(f"Przykładowe tagi: {', '.join(tags)}")


# =====================================================
# 3. promote_chat_member z can_manage_tags
# =====================================================
# Nowe uprawnienie API 9.5 do zarządzania tagami

@router.command("promote_with_tags")
async def promote_with_tag_management(ctx: Context):
    """Promocja użytkownika z uprawnieniem do zarządzania tagami"""
    
    user_id = ctx.user_id  # W prawdziwym kodzie użyj innego user_id
    
    success = await ctx.client.promote_chat_member(
        chat_id=ctx.chat_id,
        user_id=user_id,
        can_manage_chat=True,
        can_delete_messages=True,
        can_restrict_members=True,
        can_invite_users=True,
        can_manage_tags=True,  # NOWE w API 9.5!
        can_promote_members=False
    )
    
    if success:
        await ctx.reply("✅ Użytkownik promowany z uprawnieniem do zarządzania tagami!")
    else:
        await ctx.reply("❌ Nie udało się promować użytkownika")


# =====================================================
# 4. sender_tag - Tag nadawcy wiadomości
# =====================================================
# API 9.5 dodaje pole sender_tag do obiektu Message

@router.message()
async def show_sender_tag(ctx: Context):
    """Wyświetla sender_tag z wiadomości (jeśli istnieje)"""
    
    # Sprawdź czy wiadomość ma sender_tag
    if hasattr(ctx.message, 'sender_tag') and ctx.message.sender_tag:
        await ctx.reply(f"🏷️ Tag nadawcy: {ctx.message.sender_tag}")
    else:
        await ctx.reply("📝 Ta wiadomość nie ma tagu nadawcy")


# =====================================================
# 5. icon_custom_emoji_id - Custom emoji w przyciskach
# =====================================================
# API 9.5 pozwala dodawać custom emoji do przycisków

@router.command("emoji_buttons")
async def custom_emoji_buttons(ctx: Context):
    """Przykład przycisków z custom emoji (API 9.5)"""
    
    # InlineKeyboardButton z custom emoji
    inline_keyboard = InlineKeyboardMarkup.row(
        InlineKeyboardButton(
            text="🎯 Kliknij mnie",
            callback_data="click_me",
            icon_custom_emoji_id="5368324170646659234"  # Custom emoji ID
        ),
        InlineKeyboardButton(
            text="⭐ Ulubione",
            callback_data="favorite",
            icon_custom_emoji_id="5368324170646659235"
        )
    )
    
    await ctx.reply(
        "Przyciski z custom emoji:",
        reply_markup=inline_keyboard
    )


@router.command("reply_emoji")
async def reply_keyboard_with_emoji(ctx: Context):
    """ReplyKeyboard z custom emoji (BottomButton API 9.5)"""
    
    # ReplyKeyboardButton z custom emoji
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(
        "📊 Statystyki",
        "⚙️ Ustawienia"
    )
    
    # Aby dodać custom emoji, użyj obiektu ReplyKeyboardButton
    keyboard_with_emoji = ReplyKeyboardMarkup(
        keyboard=[
            [
                ReplyKeyboardButton(
                    text="🎮 Graj",
                    icon_custom_emoji_id="5368324170646659240"
                ),
                ReplyKeyboardButton(
                    text="🏆 Ranking",
                    icon_custom_emoji_id="5368324170646659241"
                )
            ]
        ],
        resize_keyboard=True
    )
    
    await ctx.reply(
        "Wybierz opcję:",
        reply_markup=keyboard_with_emoji
    )


# =====================================================
# 6. Composite Examples - Połączone funkcje
# =====================================================

@router.command("tagged_message")
async def send_tagged_message(ctx: Context):
    """Wysyłanie wiadomości z tagiem i custom emoji button"""
    
    # Najpierw ustaw tag
    await ctx.client.set_chat_member_tag(
        chat_id=ctx.chat_id,
        user_id=ctx.user_id,
        tag="active_user"
    )
    
    # Następnie wyślij wiadomość z przyciskiem emoji
    keyboard = InlineKeyboardMarkup.row(
        InlineKeyboardButton(
            text="✨ Sprawdź swój tag",
            callback_data="check_my_tag",
            icon_custom_emoji_id="5368324170646659250"
        )
    )
    
    await ctx.reply(
        "🏷️ Twój tag został ustawiony! Kliknij przycisk aby sprawdzić.",
        reply_markup=keyboard
    )


@router.callback_query()
async def handle_tag_callback(ctx: Context):
    """Obsługa callback z sprawdzaniem tagu"""
    
    if ctx.callback_query.data == "check_my_tag":
        # Pobierz informacje o członku z tagiem
        chat_member = await ctx.client.get_chat_member(
            chat_id=ctx.chat_id,
            user_id=ctx.user_id
        )
        
        # Sprawdź tag (jeśli exists)
        tag = chat_member.get('tag', 'brak tagu')
        
        await ctx.answer_callback(
            text=f"Twój tag: {tag}",
            show_alert=True
        )


# =====================================================
# 7. MessageEntity date_time type (API 9.5)
# =====================================================

@router.command("datetime_entity")
async def datetime_entity_example(ctx: Context):
    """
    Przykład użycia nowego typu encji date_time (API 9.5)
    
    MessageEntity type "date_time" pozwala botom wyświetlać
    sformatowaną datę i czas użytkownikowi.
    """
    
    from telegram_async.telegram_types import MessageEntity
    
    # Utwórz encję date_time
    # W prawdziwej aplikacji Telegram sam rozpoznaje daty w tekście
    # i tworzy odpowiednie encje
    
    await ctx.reply(
        "📅 Następne spotkanie: 2026-03-15 o 14:30\n"
        "Encja date_time pozwala na klikalne daty w wiadomościach!"
    )


# =====================================================
# Main
# =====================================================

dp.include_router(router)

async def main():
    print("🤖 Bot z obsługą API 9.5 uruchomiony!")
    print("\nDostępne komendy:")
    print("  /stream - Przykład streamowania wiadomości")
    print("  /stream_progress - Przykład z progress mode")
    print("  /set_tag - Ustaw tag dla użytkownika")
    print("  /set_admin_tag - Przykłady tagów")
    print("  /promote_with_tags - Promocja z can_manage_tags")
    print("  /emoji_buttons - Przyciski z custom emoji")
    print("  /reply_emoji - Reply keyboard z custom emoji")
    print("  /tagged_message - Wiadomość z tagiem")
    print("  /datetime_entity - Przykład encji date_time")
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
