import json

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default.main_menu import build_keyboards_post_create, build_keyboards_menu, build_post_confirm, \
    build_keyboards__cencelmenu
from loader import dp, db, bot
from aiogram import types

from states.registrations import CreatePost, SavePosts
from utils.misc.translates import tarjimon_language


@dp.message_handler(text=["📑 Post yaratish", "📑 Создание поста"])
async def create_post_menu(message: types.Message):
    tg_id = message.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)
    await message.answer(tarjimon_language("Post turini tanglang!", check_lang), reply_markup=build_keyboards_post_create(check_lang))
    await CreatePost.next()

@dp.message_handler(text=["❌ Bekor qilish"], state=CreatePost)
async def create_post_cancel_menu(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)
    await state.finish()
    await message.answer(tarjimon_language("Post yaratish bekor qilindi!", check_lang), reply_markup=build_keyboards_menu(check_lang))


@dp.message_handler(state=CreatePost.choose_post_type)
async def choose_post_type(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)
    post_type = message.text
    if post_type == "◀️ Ortga":
        await state.finish()
        await message.answer(tarjimon_language(f"Bo'limni tanglang!", check_lang),
                             reply_markup=build_keyboards_menu(check_lang))
    else:
        if post_type == "📝 Matn":
            await message.answer(tarjimon_language("Post matnini yuboring.", check_lang), reply_markup=build_keyboards__cencelmenu(check_lang))

        elif post_type == "📸 Rasm":
            await message.answer(tarjimon_language("Post rasmini yuboring.", check_lang), reply_markup=build_keyboards__cencelmenu(check_lang))

        elif post_type == "🎞 Gif":
                await message.answer(tarjimon_language("Post gifni yuboring.", check_lang), reply_markup=build_keyboards__cencelmenu(check_lang))

        elif post_type == "📹 Video":
            await message.answer(tarjimon_language("Post videoni yuboring.", check_lang), reply_markup=build_keyboards__cencelmenu(check_lang))
        await state.update_data({"post_type": post_type})
        await CreatePost.next()



@dp.message_handler(state=CreatePost.post_title_link, content_types=types.ContentType.ANY)
async def post_title_link(message: types.Message, state: FSMContext):
    info = ("Tugma uchun havolani quyidagicha formatda yuboring.\n"
         "<code>[tugma matni+https://t.me/cleancoder_uz]</code>\n"
         "Tugma qo'shmoqchi bo'lsangiz bir qatordan shu ko'rinishda havolani yuboring.\n"
         "<code>[birinchi matni+https://t.me/cleancoder_uz]</code>\n"
         "<code>[ikkinchi matni+https://t.me/cleancoder_uz]</code>")
    tg_id = message.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)
    data = await state.get_data()
    post_type = data.get('post_type')
    if post_type == "📸 Rasm":
        if message.photo:
            await state.update_data(post_content=message.photo[-1].file_id,
                                    post_caption=message.caption)
            await message.answer_photo(photo=message.photo[-1].file_id,
                                      caption=message.caption)
            await message.answer(tarjimon_language(info, check_lang))
        else:
            await message.answer(tarjimon_language("Iltimos, rasm yuboring."), check_lang)
            return

    elif post_type == "📹 Video":
        if message.video:

            await state.update_data(post_content=message.video.file_id,
                                    post_caption=message.caption)
            await message.answer_video(video=message.video.file_id,
                                      caption=message.caption)
            await message.answer(tarjimon_language(info, check_lang))
        else:
            await message.answer(tarjimon_language("Iltimos, video yuboring.", check_lang))
            return

    elif post_type == "📝 Matn":
        if message.text:
            await state.update_data(post_content=str(message.message_id))
            await message.answer(tarjimon_language(info, check_lang))
        else:
            await message.answer(tarjimon_language("Iltimos, matn yuboring.", check_lang))
            return

    elif post_type == "🎞 Gif":
        if message.animation:
            await state.update_data(post_content=message.animation.file_id,
                                    post_caption=message.caption)
            await message.answer_animation(animation=message.animation.file_id,
                                          caption=message.caption)
            await message.answer(tarjimon_language(info, check_lang))
        else:
            await message.answer(tarjimon_language("Iltimos, GIF yuboring.", check_lang))
            return

    else:
        await message.answer(tarjimon_language("Iltimos, mos keladigan kontent turini tanlang va yuboring.", check_lang))
        return

    await CreatePost.next()


@dp.message_handler(state=CreatePost.send_buttons)
async def process_buttons(message: types.Message, state: FSMContext):
    tg_id = message.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)

    if message.text == "❌ Bekor qilish" or message.text == "❌ Отмена":
        data = await state.get_data()
        post_message_id = data.get("post_message_id")
        if post_message_id:
            try:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=post_message_id)
            except Exception as e:
                await message.answer(tarjimon_language("Postni o'chirishda xatolik yuz berdi:", check_lang), e)

        await state.finish()
        await message.answer(tarjimon_language("Post yaratish bekor qilindi!", check_lang),
                             reply_markup=build_keyboards_menu(check_lang))
    elif message.text == "✅ Tasdiqlash" or message.text == "✅ Подтверждение":
        data = await state.get_data()
        post_type = data.get('post_type')
        post_content = data.get('post_content')
        post_caption = data.get('post_caption')
        buttons = data.get('buttons')
        post_id = await db.add_postbot_post(post_type, post_content, post_caption, buttons, telegram_id=tg_id)
        send_info_markup = types.InlineKeyboardMarkup(row_width=2)
        send_info_markup.add(
            types.InlineKeyboardButton(text=tarjimon_language("Ulashish", check_lang), switch_inline_query=f"{post_id}"),
            types.InlineKeyboardButton(text=tarjimon_language("Saqlash", check_lang), callback_data=f"save_post_{post_id}")
        )
        await message.answer(
            tarjimon_language("Postingiz tayyor!\n\n"
            f"Siz uni quyidagi kod orqali istalgan chatda ishlatishingiz mumkin:!", check_lang),
            reply_markup=send_info_markup
        )
        await message.answer(
            f"@new_test2023Bot <code>{post_id}</code>", reply_markup=build_keyboards_menu(check_lang)
        )
        await state.finish()
    else:
        button_text = message.text
        button_texts = button_text.split('\n')
        buttons = []
        for btn in button_texts:
            if not (btn.startswith('[') and btn.endswith(']') and '+' in btn):
                await message.answer(tarjimon_language("Iltimos, tugmalarni quyidagi formatda kiriting:\n"
                                     "<code>[tugma matni+https://t.me/cleancoder_uz]</code>\n"
                                     "<code>[birinchi matni+https://t.me/cleancoder_uz]</code>\n"
                                     "<code>[ikkinchi matni+https://t.me/cleancoder_uz]</code>", check_lang))
                return
            clean_name = btn[1:-1]
            try:
                button_name, button_url = clean_name.split('+', 1)
            except ValueError:
                await message.answer(
                    tarjimon_language("Xato format:", check_lang), btn,
                    tarjimon_language("Iltimos, <code>[tugma matni+https://t.me/cleancoder_uz]</code> formatida kiriting.", check_lang))
                return
            buttons.append({'text': button_name, 'url': button_url})
        data = await state.get_data()
        all_buttons = data.get("buttons", [])
        all_buttons.extend(buttons)
        await state.update_data(buttons=all_buttons)
        inline_kb = InlineKeyboardMarkup()
        for btn in all_buttons:
            inline_kb.add(InlineKeyboardButton(text=btn['text'], url=btn['url']))
        await message.answer(tarjimon_language("Kerakli tugmalardan birini tanlang:", check_lang), reply_markup=build_post_confirm(check_lang))


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("save_post_"))
async def handle_save_post(callback_query: types.CallbackQuery, state: FSMContext):
    post_id = callback_query.data.split("_")[2]
    tg_id = callback_query.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)

    await state.update_data(post_id=post_id)
    post_exists = await db.get_postbot_post_by_id_saves(post_id=int(post_id))
    if post_exists:
        await callback_query.answer(tarjimon_language("Post avval saqlangan.", check_lang), show_alert=True)
        return
    else:
        await state.update_data(post_id=post_id)
        post = await db.get_post_by_id(int(post_id))
        if post:
            await callback_query.message.answer(tarjimon_language("Post uchun qisqa nom bering:", check_lang))
            await SavePosts.next()

@dp.message_handler(state=SavePosts.postname)
async def save_postname(message: types.Message, state: FSMContext):
    data = await state.get_data()
    post_id = data.get("post_id")
    post_name = message.text
    tg_id = message.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)
    if not post_name:
        await message.answer(tarjimon_language("Post nomi bo'sh bo'lishi mumkin emas.", check_lang))
        return
    await state.update_data(post_name=post_name)
    try:
        await db.add_postbot_post_saves(
            post_name=post_name,
            post_id=int(post_id),
            telegram_id=message.from_user.id
        )
        await message.answer(tarjimon_language("Post saqlandi.", check_lang), reply_markup=build_keyboards_menu(check_lang))
        await state.finish()
    except Exception:
        pass


@dp.inline_handler()
async def handle_inline_query(inline_query: types.InlineQuery):
    post_id = inline_query.query.strip()
    tg_id = inline_query.from_user.id
    check_lang = await db.check_lang_postbot_users(telegram_id=tg_id)
    if not post_id:
        result = types.InlineQueryResultArticle(
            id="1",
            title=tarjimon_language("Post ID yuborish", check_lang),
            input_message_content=types.InputTextMessageContent(
                message_text=tarjimon_language("Iltimos, post ID yuboring.", check_lang)
            )
        )
        await bot.answer_inline_query(inline_query.id, results=[result])
        return

    try:
        post_id_int = int(post_id)
        posts = await db.get_post_by_idtg_id(post_id=post_id_int, tg_id=tg_id)
        if not posts:
            result = types.InlineQueryResultArticle(
                id="2",
                title=tarjimon_language("Post topilmadi", check_lang),
                input_message_content=types.InputTextMessageContent(
                    message_text=tarjimon_language("Post topilmadi. Iltimos, boshqa post ID yuboring.", check_lang)
                )
            )
            await bot.answer_inline_query(inline_query.id, results=[result])
            return

        post_type = posts["post_type"]
        post_content = posts["post_content"]
        post_caption = posts["post_caption"]
        buttons = json.loads(posts["buttons"])
        share_markup = types.InlineKeyboardMarkup(row_width=2)
        for button in buttons:
            if isinstance(button, dict) and 'text' in button and 'url' in button:
                share_markup.add(types.InlineKeyboardButton(text=button['text'], url=button['url']))

        if post_type == "📝 Matn":
            inline_query_result = types.InlineQueryResultArticle(
                id=str(post_id),
                title="Matn Post",
                input_message_content=types.InputTextMessageContent(message_text=post_content),
                reply_markup=share_markup
            )
        elif post_type == "📸 Rasm":
            inline_query_result = types.InlineQueryResultPhoto(
                id=str(post_id),
                photo_url=post_content,
                thumb_url=post_content,
                title="Rasm Post",
                caption=post_caption or "",
                reply_markup=share_markup
            )
        elif post_type == "📹 Video":
            inline_query_result = types.InlineQueryResultVideo(
                id=str(post_id),
                video_url=post_content,
                thumb_url=post_content,
                title="Video Post",
                caption=post_caption or "",
                mime_type="video/mp4",
                reply_markup=share_markup
            )
        elif post_type == "🎞 Gif":
            inline_query_result = types.InlineQueryResultGif(
                id=str(post_id),
                gif_url=post_content,
                thumb_url=post_content,
                title="GIF Post",
                caption=post_caption or "",
                reply_markup=share_markup
            )
        else:
            result = types.InlineQueryResultArticle(
                id="3",
                title=tarjimon_language("Xato", check_lang),
                input_message_content=types.InputTextMessageContent(
                    message_text=tarjimon_language("Noto'g'ri post turi. Iltimos, to'g'ri post ID yuboring.",
                                                   check_lang)
                )
            )
            await bot.answer_inline_query(inline_query.id, results=[result])
            return

        await bot.answer_inline_query(inline_query.id, results=[inline_query_result])

    except ValueError:
        result = types.InlineQueryResultArticle(
            id="4",
            title=tarjimon_language("Xato", check_lang),
            input_message_content=types.InputTextMessageContent(
                message_text=tarjimon_language("Post ID noto'g'ri formatda. Iltimos, raqamli post ID yuboring.", check_lang)
            )
        )
        await bot.answer_inline_query(inline_query.id, results=[result])