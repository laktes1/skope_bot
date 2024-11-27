from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главная клавиатура
reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Manager"), KeyboardButton(text="Admin")],  # Две кнопки в строке
    ],
    resize_keyboard=True
)

# Инлайн-клавиатура для "Manager"
keyboard_manager = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Найти пользователя", callback_data="find_user")],
    ]
)

# Клавиатура для перехода в админку
keyboard_admin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Админ панель")],
    ],
    resize_keyboard=True
)