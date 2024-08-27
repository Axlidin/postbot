from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.default.main_menu import build_keyboards_menu
from loader import dp, db
from aiogram import types
from utils.misc.translates import tarjimon_language


@dp.message_handler(text=["🌟 Sara postlarim", "🌟 Лучшие мои посты"])
async def show_saved_posts(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)
    saved_posts = await db.get_posts_tg_id(tg_id=tg_id)
    yashir = InlineKeyboardMarkup()
    yashir.add(InlineKeyboardButton(text=tarjimon_language("Yashirish", check_lang), callback_data="yashirish"))
    if not saved_posts:
        await message.answer(tarjimon_language("Sizda saqlangan postlar yoq!", check_lang))
        return

    msg = f""
    for number, post in enumerate(saved_posts, 1):
        msg += f"{number}. {post['post_name']}\n"
        msg += f"<code>@Pb_post_bot {post['post_id']}</code>\n"
        msg += f"🗑 /delete_{post['post_id']}"
    await message.answer(msg, reply_markup=yashir)

@dp.callback_query_handler(lambda c: c.data == "yashirish" or c.data == "Скрывать")
async def yashir_menu(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    tg_id = callback_query.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)
    await callback_query.message.answer(tarjimon_language(f"Bo'limni tanglang!", check_lang),
                              reply_markup=build_keyboards_menu(check_lang))


@dp.message_handler(lambda message: message.text.startswith('/delete_'))
async def delete_post(message: types.Message):
    tg_id = message.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)
    command = message.text[len('/delete_'):]
    try:
        post_id = int(command)
        tg_id = message.from_user.id
        await db.delete_post_by_id(post_id=post_id, tg_id=tg_id)
        await message.answer(tarjimon_language("Postni o'chirdingiz!", check_lang), reply_markup=build_keyboards_menu(check_lang))
    except ValueError:
        await message.answer(tarjimon_language("Post ID noto'g'ri formatda!", check_lang), reply_markup=build_keyboards_menu(check_lang))
    except Exception:
        await message.answer(tarjimon_language("Xatolik yuz berdi, postni o'chirishda!", check_lang), reply_markup=build_keyboards_menu(check_lang))


@dp.message_handler(text=["🇺🇿 Til", "🇷🇺 Язык"])
async def user_changeLang(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)
    if check_lang == '🇺🇿':
        new_lang = '🇷🇺'
    elif check_lang == '🇷🇺':
        new_lang = '🇺🇿'
    else:
        new_lang = '🇺🇿'
    try:
        await db.update_user_language_postbot_users(telegram_id=tg_id, new_lang=new_lang)
        await state.update_data({"lang_code": new_lang})
        success_message = tarjimon_language("Tilingiz o'zgartirildi!", new_lang)
        await message.answer(success_message, reply_markup=build_keyboards_menu(new_lang))
    except Exception:
        await message.answer(tarjimon_language("Tilni yangilashdagi xato", check_lang))
