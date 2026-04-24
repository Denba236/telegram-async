# 🎨 Colored Buttons - Цветные кнопки в Telegram Bot API 9.4+

## 📋 Обзор

Начиная с **Bot API 9.4** (9 февраля 2026), Telegram позволяет задавать **цвет кнопок** через параметр `style`.

Это работает как для **InlineKeyboardButton**, так и для **ReplyKeyboardButton**.

---

## ✅ Реализовано

### Поддерживаемые стили (цвета):

| Стиль | Цвет | Значение |
|-------|------|----------|
| `primary` | 🔵 **Синий** | Основные действия, навигация |
| `success` | 🟢 **Зеленый** | Подтверждение, успех, активация |
| `danger` | 🔴 **Красный** | Удаление, отмена, опасность |

**По умолчанию:** Если `style` не указан, применяется app-specific default style (обычно серый/белый).

---

## 🚀 Как использовать

### 1. InlineKeyboardButton с цветом

```python
from telegram_async.keyboards import InlineKeyboardButton, InlineKeyboardMarkup

# Синяя кнопка (primary)
btn = InlineKeyboardButton(
    text="📊 Статистика",
    callback_data="stats",
    style=InlineKeyboardButton.STYLE_PRIMARY  # или style="primary"
)

# Зеленая кнопка (success)
btn = InlineKeyboardButton(
    text="✅ Подтвердить",
    callback_data="confirm",
    style=InlineKeyboardButton.STYLE_SUCCESS  # или style="success"
)

# Красная кнопка (danger)
btn = InlineKeyboardButton(
    text="🗑️ Удалить",
    callback_data="delete",
    style=InlineKeyboardButton.STYLE_DANGER  # или style="danger"
)

# Клавиатура с разными цветами
keyboard = InlineKeyboardMarkup.row(
    InlineKeyboardButton(
        text="✅ Подтвердить",
        callback_data="confirm",
        style="success"
    ),
    InlineKeyboardButton(
        text="❌ Отмена",
        callback_data="cancel",
        style="danger"
    )
)
```

### 2. ReplyKeyboardButton с цветом

```python
from telegram_async.keyboards import ReplyKeyboardButton, ReplyKeyboardMarkup

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            ReplyKeyboardButton(
                text="▶️ Играть",
                style=ReplyKeyboardButton.STYLE_SUCCESS  # Зеленый
            ),
            ReplyKeyboardButton(
                text="⏹️ Стоп",
                style=ReplyKeyboardButton.STYLE_DANGER  # Красный
            )
        ],
        [
            ReplyKeyboardButton(
                text="⚙️ Настройки",
                style=ReplyKeyboardButton.STYLE_PRIMARY  # Синий
            )
        ]
    ],
    resize_keyboard=True
)
```

---

## 📝 Полные примеры

### Пример 1: Диалог подтверждения

```python
@router.command("delete")
async def delete_confirmation(ctx: Context):
    keyboard = InlineKeyboardMarkup.row(
        InlineKeyboardButton(
            text="✅ Да, удалить",
            callback_data="confirm_delete",
            style="danger"  # Красный - опасное действие
        ),
        InlineKeyboardButton(
            text="❌ Отмена",
            callback_data="cancel_delete",
            style="primary"  # Синий - отмена
        )
    )
    
    await ctx.reply(
        "⚠️ Вы уверены, что хотите удалить этот файл?\n"
        "Это действие нельзя отменить.",
        reply_markup=keyboard
    )
```

### Пример 2: Игровые контролы

```python
@router.command("game")
async def game_controls(ctx: Context):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                ReplyKeyboardButton(
                    text="▶️ Играть",
                    style="success"  # Зеленый - начать
                )
            ],
            [
                ReplyKeyboardButton(
                    text="⏸️ Пауза",
                    style="primary"  # Синий - нейтральное
                ),
                ReplyKeyboardButton(
                    text="⏹️ Стоп",
                    style="danger"  # Красный - остановить
                )
            ]
        ],
        resize_keyboard=True
    )
    
    await ctx.reply("🎮 Управление игрой:", reply_markup=keyboard)
```

### Пример 3: Админ панель

```python
@router.command("admin")
async def admin_panel(ctx: Context):
    keyboard = InlineKeyboardMarkup()
    
    # Синие кнопки - навигация
    keyboard.add(
        InlineKeyboardButton(
            text="👥 Пользователи",
            callback_data="users",
            style="primary",
            icon_custom_emoji_id="5368324170646659234"
        ),
        InlineKeyboardButton(
            text="📊 Статистика",
            callback_data="stats",
            style="primary",
            icon_custom_emoji_id="5368324170646659235"
        )
    )
    
    # Зеленая кнопка - одобрить
    keyboard.add(
        InlineKeyboardButton(
            text="✅ Одобрить всех",
            callback_data="approve_all",
            style="success"
        )
    )
    
    # Красные кнопки - опасные действия
    keyboard.add(
        InlineKeyboardButton(
            text="🗑️ Удалить спам",
            callback_data="delete_spam",
            style="danger"
        ),
        InlineKeyboardButton(
            text="⛔ Бан нарушителей",
            callback_data="ban_users",
            style="danger"
        )
    )
    
    await ctx.reply("👨‍💼 Панель администратора:", reply_markup=keyboard)
```

### Пример 4: Контекстные цвета

```python
@router.command("pay")
async def payment_button(ctx: Context):
    user_balance = 10  # Пример баланса
    
    # Меняем цвет в зависимости от баланса
    if user_balance > 50:
        style = "success"  # Зеленый - достаточно средств
        text = "✅ Оплатить (баланс OK)"
    else:
        style = "danger"  # Красный - мало средств
        text = "⚠️ Оплатить (мало средств)"
    
    keyboard = InlineKeyboardMarkup.row(
        InlineKeyboardButton(
            text=text,
            callback_data="pay",
            style=style
        )
    )
    
    await ctx.reply(f"💰 Ваш баланс: {user_balance}", reply_markup=keyboard)
```

---

## 🎯 Лучшие практики

### ✅ Правильное использование:

**Primary (Синий):**
- Основные действия в приложении
- Навигация между разделами
- Информационные кнопки
- Нейтральные действия

```python
InlineKeyboardButton("📊 Статистика", callback_data="stats", style="primary")
InlineKeyboardButton("⚙️ Настройки", callback_data="settings", style="primary")
```

**Success (Зеленый):**
- Подтверждение действий
- Успешные операции
- Активация функций
- Положительные ответы

```python
InlineKeyboardButton("✅ Подтвердить", callback_data="confirm", style="success")
InlineKeyboardButton("✓ Одобрить", callback_data="approve", style="success")
```

**Danger (Красный):**
- Удаление данных
- Отмена действий
- Критические операции
- Предупреждения

```python
InlineKeyboardButton("🗑️ Удалить", callback_data="delete", style="danger")
InlineKeyboardButton("⛔ Бан", callback_data="ban", style="danger")
```

### ❌ Неправильное использование:

```python
# ❌ Не используйте danger для обычных действий
InlineKeyboardButton("📊 Статистика", callback_data="stats", style="danger")  # ПЛОХО!

# ❌ Не используйте success для удаления
InlineKeyboardButton("🗑️ Удалить", callback_data="delete", style="success")  # ПЛОХО!

# ✅ Логичное использование
InlineKeyboardButton("🗑️ Удалить", callback_data="delete", style="danger")  # ХОРОШО!
InlineKeyboardButton("✅ Подтвердить", callback_data="confirm", style="success")  # ХОРОШО!
```

---

## 💡 Комбинация с другими функциями

### С custom emoji (API 9.5):

```python
InlineKeyboardButton(
    text="🎮 Играть",
    callback_data="play",
    style="success",                          # Цвет кнопки
    icon_custom_emoji_id="5368324170646659234"  # + custom emoji
)
```

### С Web App:

```python
InlineKeyboardButton(
    text="🛒 Магазин",
    web_app={"url": "https://shop.example.c
             m"},
    style="primary"
)
```

### С URL:

```python
InlineKeyboardButton(
    text="🔗 Документация",
    url="https://example.com/docs",
    style="primary"
)
```

---

## 📊 Сравнение: До и После

### ❌ Без цветов (старый способ):

```python
keyboard = InlineKeyboardMarkup.row(
    InlineKeyboardButton(text="Подтвердить", callback_data="confirm"),
    InlineKeyboardButton(text="Отмена", callback_data="cancel")
)
```
**Результат:** Обе кнопки одинаковые, пользователь не видит разницы.

### ✅ С цветами (API 9.4+):

```python
keyboard = InlineKeyboardMarkup.row(
    InlineKeyboardButton(
        text="✅ Подтвердить", 
        callback_data="confirm",
        style="success"  # 🟢 Зеленый
    ),
    InlineKeyboardButton(
        text="❌ Отмена", 
        callback_data="cancel",
        style="danger"  # 🔴 Красный
    )
)
```
**Результат:** Цвета сразу показывают назначение кнопок!

---

## 🔍 Технические детали

### Расположение в коде:

**InlineKeyboardButton:**
```
keyboards/inline.py
├── style: Optional[Literal["primary", "success", "danger"]]
├── STYLE_PRIMARY = "primary"
├── STYLE_SUCCESS = "success"
└── STYLE_DANGER = "danger"
```

**ReplyKeyboardButton:**
```
keyboards/reply.py
├── style: Optional[Literal["primary", "success", "danger"]]
├── STYLE_PRIMARY = "primary"
├── STYLE_SUCCESS = "success"
└── STYLE_DANGER = "danger"
```

### Сериализация:

```python
# to_dict() автоматически включает style
btn = InlineKeyboardButton(text="Click", callback_data="x", style="primary")
print(btn.to_dict())
# {'text': 'Click', 'callback_data': 'x', 'style': 'primary'}
```

---

## ⚠️ Важные заметки

1. **Все стили опциональны** - кнопка работает и без `style`
2. **Цвета задаются Telegram** - вы не можете задать произвольный цвет
3. **Только 3 стиля** - primary, success, danger
4. **Custom emoji + style** - можно использовать вместе!
5. **Работает везде** - inline и reply клавиатуры

---

## 📚 Дополнительные ресурсы

- **examples_colored_buttons.py** - Полный пример с цветными кнопками
- **API_95_CHANGES.md** - Общая документация по API 9.5
- **QUICK_REFERENCE_95.md** - Быстрая справка
- [Official Bot API 9.4 Changelog](https://core.telegram.org/bots/api-changelog#february-9-2026)
- [InlineKeyboardButton Docs](https://core.telegram.org/bots/api#inlinekeyboardbutton)
- [KeyboardButton Docs](https://core.telegram.org/bots/api#keyboardbutton)

---

## 🎨 Галерея цветов

### InlineKeyboardButton:

```
🔵 Primary:   [ Синяя кнопка ]
🟢 Success:   [ Зеленая кнопка ]
🔴 Danger:    [ Красная кнопка ]
⚪ Default:   [ Обычная кнопка ]
```

### ReplyKeyboardButton:

```
┌──────────────────────┐
│ 🔵 Primary кнопка    │  ← Синий
│ 🟢 Success кнопка    │  ← Зеленый
│ 🔴 Danger кнопка     │  ← Красный
│ ⚪ Обычная кнопка    │  ← Default
└──────────────────────┘
```

---

## 🚀 Готово к использованию!

Функция цветных кнопок полностью реализована в вашей библиотеке. Просто используйте параметр `style` при создании кнопок!

```python
# Быстрый старт
btn = InlineKeyboardButton(
    text="🎮 Начать игру",
    callback_data="start",
    style="success"  # Вот и всё! 🟢
)
```

**Happy coding with colors! 🎨**
