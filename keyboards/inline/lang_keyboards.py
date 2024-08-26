from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

lang_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺", callback_data="lang_ru"),
        ]
    ]
)