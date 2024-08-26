from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.misc.translates import tarjimon_language


def build_keyboards_menu(request):
    menu_text = [
        ["🌟 Sara postlarim", "📑 Post yaratish"],
        ["🇺🇿 Til"]
    ]

    translated_menu_text = [[tarjimon_language(text, request) for text in row] for row in menu_text]

    MainMenuKeyborads = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text) for text in row] for row in translated_menu_text
        ], resize_keyboard=True,
        one_time_keyboard=True,
    )
    return MainMenuKeyborads

def build_keyboards_post_create(request):
    post_create_menu_text = [
        ["📝 Matn", "📸 Rasm"],
        ["🎞 Gif", "📹 Video"],
        ["◀️ Ortga"]
    ]
    translated_post_create_menu_text = [[tarjimon_language(text, request) for text in row] for row in post_create_menu_text]
    PostCreateKeyborads = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text) for text in row] for row in translated_post_create_menu_text
        ], resize_keyboard=True,
        one_time_keyboard=True,
    )
    return PostCreateKeyborads


def build_keyboards__cencelmenu(request):
    post_create_menu_text = [
        ["❌ Bekor qilish"]
    ]
    translated_post_create_menu_text = [[tarjimon_language(text, request) for text in row] for row in post_create_menu_text]
    PostCreateKeyborads = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text) for text in row] for row in translated_post_create_menu_text
        ], resize_keyboard=True,
        one_time_keyboard=True,
    )
    return PostCreateKeyborads


def build_post_confirm(request):
    post_confirm_menu_text = [
        ["✅ Tasdiqlash", "❌ Bekor qilish"],
    ]
    translated_post_confirm_menu_text = [[tarjimon_language(text, request) for text in row] for row in post_confirm_menu_text]
    PostConfirmKeyborads = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text) for text in row] for row in translated_post_confirm_menu_text
        ], resize_keyboard=True,
        one_time_keyboard=True,
    )
    return PostConfirmKeyborads