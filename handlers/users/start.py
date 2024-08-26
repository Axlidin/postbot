from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.main_menu import build_keyboards_menu
from states.registrations import RegistrationStates, Sozlamalar
from utils.misc.translates import tarjimon_language
from keyboards.inline.lang_keyboards import lang_keyboard
from loader import dp, bot, db

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    tg_id = message.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)
    if check_lang:
        await message.answer(tarjimon_language(f"Bo'limni tanglang!", check_lang),
                             reply_markup=build_keyboards_menu(check_lang))
    else:
        await message.answer(tarjimon_language('Tilni tanlang!'), reply_markup=lang_keyboard)
        await RegistrationStates.next()

# Foydalanuvchining tilini o'zgartirishga state boshladik
@dp.callback_query_handler(state=RegistrationStates.language, text_contains='lang_')
async def change_language(call: types.CallbackQuery, state: FSMContext):
    lang_code = call.data[5:]
    await state.update_data(
        {"lang_code": lang_code}
    )
    tg_id = call.from_user.id
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(tarjimon_language(f"Bo'limni tanglang!", lang_code),
                              reply_markup=build_keyboards_menu(lang_code))
    data = await state.get_data()
    lang_code = data.get("lang_code")
    try:
        await db.add_postbot_users(
            users_language=lang_code,
            fullname=call.from_user.full_name,
            telegram_id=tg_id
        )
    except Exception:
        pass
    await state.finish()
