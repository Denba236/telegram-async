"""
Примеры использования цветных кнопок (Colored Buttons) - API 9.4+

Telegram API 9.4+ позволяет задавать цвет кнопок через параметр style.

Доступные стили (цвета):
- "primary"   → Синий цвет (основной)
- "success"   → Зеленый цвет (успех/подтверждение)
- "danger"    → Красный цвет (опасность/удаление)

Цвета работают как в InlineKeyboardButton, так и в ReplyKeyboardButton.
"""

import asyncio
from telegram_async import Bot, Dispatcher, Context
from telegram_async.dispatcher.router import Router
from telegram_async.keyboards import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, ReplyKeyboardButton
)

bot = Bot("TOKEN")
dp = Dispatcher()
router = Router(name="colored_buttons_examples")


# =====================================================
# 1. InlineKeyboardButton с цветами
# =====================================================

@router.command("colored_inline")
async def colored_inline_buttons(ctx: Context):
    """Пример inline клавиатуры с цветными кнопками"""
    
    keyboard = InlineKeyboardMarkup()
    
    # Синяя кнопка (primary)
    keyboard.add(
        InlineKeyboardButton(
            text="🔵 Основная кнопка",
            callback_data="primary_action",
            style=InlineKeyboardButton.STYLE_PRIMARY  # Синий
        )
    )
    
    # Зеленая кнопка (success)
    keyboard.add(
        InlineKeyboardButton(
            text="🟢 Подтвердить",
            callback_data="confirm",
            style=InlineKeyboardButton.STYLE_SUCCESS  # Зеленый
        )
    )
    
    # Красная кнопка (danger)
    keyboard.add(
        InlineKeyboardButton(
            text="🔴 Удалить",
            callback_data="delete",
            style=InlineKeyboardButton.STYLE_DANGER  # Красный
        )
    )
    
    # Кнопка без стиля (по умолчанию)
    keyboard.add(
        InlineKeyboardButton(
            text="⚪ Обычная кнопка",
            callback_data="default"
        )
    )
    
    await ctx.reply(
        "🎨 Цветные inline кнопки:\n\n"
        "🔵 Primary - для основных действий\n"
        "🟢 Success - для подтверждения/успеха\n"
        "🔴 Danger - для удаления/опасных действий",
        reply_markup=keyboard
    )


@router.command("confirmation_dialog")
async def confirmation_with_colors(ctx: Context):
    """Диалог подтверждения с цветными кнопками"""
    
    keyboard = InlineKeyboardMarkup.row(
        InlineKeyboardButton(
            text="✅ Подтвердить",
            callback_data="confirm_yes",
            style=InlineKeyboardButton.STYLE_SUCCESS,  # Зеленый
            icon_custom_emoji_id="5368324170646659234"  # + custom emoji
        ),
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data="confirm_no",
            style=InlineKeyboardButton.STYLE_DANGER  # Красный
        )
    )
    
    await ctx.reply(
        "⚠️ Вы уверены, что хотите выполнить это действие?\n\n"
        "Это действие нельзя отменить.",
        reply_markup=keyboard
    )


@router.command("menu_colors")
async def colored_menu(ctx: Context):
    """Меню с разными цветами кнопок"""
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="📊 Статистика",
            callback_data="stats",
            style=InlineKeyboardButton.STYLE_PRIMARY,
            icon_custom_emoji_id="5368324170646659240"
        ),
        InlineKeyboardButton(
            text="⚙️ Настройки",
            callback_data="settings",
            style=InlineKeyboardButton.STYLE_PRIMARY,
            icon_custom_emoji_id="5368324170646659241"
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="🚀 Запустить",
            callback_data="start_process",
            style=InlineKeyboardButton.STYLE_SUCCESS,
            icon_custom_emoji_id="5368324170646659242"
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="🗑️ Очистить кэш",
            callback_data="clear_cache",
            style=InlineKeyboardButton.STYLE_DANGER,
            icon_custom_emoji_id="5368324170646659243"
        ),
        InlineKeyboardButton(
            text="⛔ Сбросить всё",
            callback_data="reset_all",
            style=InlineKeyboardButton.STYLE_DANGER,
            icon_custom_emoji_id="5368324170646659244"
        )
    )
    
    await ctx.reply("🎨 Главное меню с цветными кнопками:", reply_markup=keyboard)


# =====================================================
# 2. ReplyKeyboardButton с цветами
# =====================================================

@router.command("colored_reply")
async def colored_reply_keyboard(ctx: Context):
    """Пример reply клавиатуры с цветными кнопками"""
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                ReplyKeyboardButton(
                    text="🔵 Основная функция",
                    style=ReplyKeyboardButton.STYLE_PRIMARY  # Синий
                ),
                ReplyKeyboardButton(
                    text="🟢 Подтвердить",
                    style=ReplyKeyboardButton.STYLE_SUCCESS  # Зеленый
                )
            ],
            [
                ReplyKeyboardButton(
                    text="🔴 Удалить",
                    style=ReplyKeyboardButton.STYLE_DANGER  # Красный
                ),
                ReplyKeyboardButton(
                    text="⚪ Обычная",
                    # Без style - по умолчанию
                )
            ]
        ],
        resize_keyboard=True
    )
    
    await ctx.reply(
        "🎨 Reply клавиатура с цветными кнопками:\n"
        "(нажмите кнопку на клавиатуре)",
        reply_markup=keyboard
    )


@router.command("game_controls")
async def game_controls_colors(ctx: Context):
    """Игровые контролы с цветами"""
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                ReplyKeyboardButton(
                    text="▶️ Играть",
                    style=ReplyKeyboardButton.STYLE_SUCCESS,  # Зеленый
                    icon_custom_emoji_id="5368324170646659250"
                )
            ],
            [
                ReplyKeyboardButton(
                    text="⏸️ Пауза",
                    style=ReplyKeyboardButton.STYLE_PRIMARY,  # Синий
                    icon_custom_emoji_id="5368324170646659251"
                ),
                ReplyKeyboardButton(
                    text="⏹️ Стоп",
                    style=ReplyKeyboardButton.STYLE_DANGER,  # Красный
                    icon_custom_emoji_id="5368324170646659252"
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    await ctx.reply("🎮 Игровые контролы:", reply_markup=keyboard)


@router.command("admin_panel")
async def admin_panel_colors(ctx: Context):
    """Админ панель с логическими цветами"""
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                ReplyKeyboardButton(
                    text="👥 Пользователи",
                    style=ReplyKeyboardButton.STYLE_PRIMARY
                ),
                ReplyKeyboardButton(
                    text="📊 Статистика",
                    style=ReplyKeyboardButton.STYLE_PRIMARY
                )
            ],
            [
                ReplyKeyboardButton(
                    text="✅ Одобрить всех",
                    style=ReplyKeyboardButton.STYLE_SUCCESS
                )
            ],
            [
                ReplyKeyboardButton(
                    text="🗑️ Удалить спам",
                    style=ReplyKeyboardButton.STYLE_DANGER
                ),
                ReplyKeyboardButton(
                    text="⛔ Бан нарушителей",
                    style=ReplyKeyboardButton.STYLE_DANGER
                )
            ],
            [
                ReplyKeyboardButton(
                    text="🔙 Закрыть панель",
                    # Без стиля
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await ctx.reply("👨‍💼 Панель администратора:", reply_markup=keyboard)


# =====================================================
# 3. Комбинированные примеры
# =====================================================

@router.command("styled_buttons")
async def all_styles_demo(ctx: Context):
    """Демонстрация всех стилей кнопок"""
    
    # Inline keyboard
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(
        InlineKeyboardButton(
            text="🔵 Primary (Синий)",
            callback_data="style_primary",
            style="primary"
        )
    )
    inline_kb.add(
        InlineKeyboardButton(
            text="🟢 Success (Зеленый)",
            callback_data="style_success",
            style="success"
        )
    )
    inline_kb.add(
        InlineKeyboardButton(
            text="🔴 Danger (Красный)",
            callback_data="style_danger",
            style="danger"
        )
    )
    inline_kb.add(
        InlineKeyboardButton(
            text="⚪ Default (без стиля)",
            callback_data="style_default"
        )
    )
    
    await ctx.reply(
        "🎨 <b>Цветные кнопки - API 9.4+</b>\n\n"
        "<b>Доступные стили:</b>\n"
        "• <code>primary</code> - синий (основной)\n"
        "• <code>success</code> - зеленый (успех)\n"
        "• <code>danger</code> - красный (опасность)\n\n"
        "<i>Inline клавиатура:</i>",
        reply_markup=inline_kb,
        parse_mode="HTML"
    )


@router.command("smart_colors")
async def smart_color_usage(ctx: Context):
    """Умное использование цветов по контексту"""
    
    # Пример: показ разных цветов в зависимости от состояния
    user_balance = 100  # Пример баланса
    
    keyboard = InlineKeyboardMarkup()
    
    if user_balance > 50:
        # Достаточно средств - зеленая кнопка
        keyboard.add(
            InlineKeyboardButton(
                text="✅ Пополнить (баланс OK)",
                callback_data="top_up",
                style=InlineKeyboardButton.STYLE_SUCCESS
            )
        )
    else:
        # Мало средств - красная кнопка (предупреждение)
        keyboard.add(
            InlineKeyboardButton(
                text="⚠️ Пополнить (мало средств)",
                callback_data="top_up",
                style=InlineKeyboardButton.STYLE_DANGER
            )
        )
    
    # Синяя кнопка для основной функции
    keyboard.add(
        InlineKeyboardButton(
            text="📊 Моя статистика",
            callback_data="stats",
            style=InlineKeyboardButton.STYLE_PRIMARY
        )
    )
    
    await ctx.reply(
        f"💰 Ваш баланс: {user_balance} монет\n\n"
        "🎨 Цвет кнопок меняется в зависимости от контекста!",
        reply_markup=keyboard
    )


# =====================================================
# 4. Обработка callback от цветных кнопок
# =====================================================

@router.callback_query()
async def handle_colored_callbacks(ctx: Context):
    """Обработка нажатий на цветные кнопки"""
    
    data = ctx.callback_query.data
    
    if data == "confirm":
        await ctx.answer_callback(
            text="✅ Действие подтверждено!",
            show_alert=True
        )
        
    elif data == "delete":
        await ctx.answer_callback(
            text="🔴 Вы нажали кнопку удаления!",
            show_alert=True
        )
        
    elif data == "primary_action":
        await ctx.answer_callback(
            text="🔵 Выполняется основное действие...",
            show_alert=False
        )
        
    elif data.startswith("style_"):
        style = data.replace("style_", "")
        style_names = {
            "primary": "🔵 Синий (Primary)",
            "success": "🟢 Зеленый (Success)",
            "d danger": "🔴 Красный (Danger)",
            "default": "⚪ Default (без стиля)"
        }
        style_name = style_names.get(style, style)
        
        await ctx.answer_callback(
            text=f"Вы нажали: {style_name}",
            show_alert=True
        )


# =====================================================
# 5. Best Practices
# =====================================================

@router.command("best_practices")
async def best_practices_colors(ctx: Context):
    """Лучшие практики использования цветов"""
    
    keyboard = InlineKeyboardMarkup()
    
    # Хороший пример: логичное использование цветов
    keyboard.add(
        InlineKeyboardButton(
            text="📝 Создать заказ",
            callback_data="create_order",
            style=InlineKeyboardButton.STYLE_PRIMARY,  # Синий - основное действие
            icon_custom_emoji_id="5368324170646659260"
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="✅ Подтвердить оплату",
            callback_data="confirm_payment",
            style=InlineKeyboardButton.STYLE_SUCCESS,  # Зеленый - успех/подтверждение
            icon_custom_emoji_id="5368324170646659261"
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="🗑️ Удалить заказ",
            callback_data="delete_order",
            style=InlineKeyboardButton.STYLE_DANGER,  # Красный - опасность/удаление
            icon_custom_emoji_id="5368324170646659262"
        )
    )
    
    await ctx.reply(
        "🎯 <b>Лучшие практики цветов:</b>\n\n"
        "🔵 <b>Primary (Синий):</b>\n"
        "• Основные действия\n"
        "• Навигация\n"
        "• Информационные кнопки\n\n"
        "🟢 <b>Success (Зеленый):</b>\n"
        "• Подтверждение\n"
        "• Успешные операции\n"
        "• Активация функций\n\n"
        "🔴 <b>Danger (Красный):</b>\n"
        "• Удаление\n"
        "• Отмена действий\n"
        "• Критические операции\n\n"
        "⚠️ <b>Советы:</b>\n"
        "• Используйте цвета логично\n"
        "• Не смешивайте без причины\n"
        "• Red кнопок = меньше тревоги",
        reply_markup=keyboard,
        parse_mode="HTML"
    )


# =====================================================
# Main
# =====================================================

dp.include_router(router)

async def main():
    print("🤖 Bot с цветными кнопками (API 9.4+) запущен!")
    print("\nДоступные команды:")
    print("  /colored_inline - Inline клавиатура с цветами")
    print("  /confirmation_dialog - Диалог подтверждения")
    print("  /menu_colors - Меню с цветными кнопками")
    print("  /colored_reply - Reply клавиатура с цветами")
    print("  /game_controls - Игровые контролы")
    print("  /admin_panel - Админ панель")
    print("  /styled_buttons - Все стили")
    print("  /smart_colors - Умное использование цветов")
    print("  /best_practices - Лучшие практики")
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
