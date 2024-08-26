translations = {
    '🇷🇺': {
        "🌟 Sara postlarim": "🌟 Лучшие мои посты",
        "📑 Post yaratish": "📑 Создание поста",
        "🇺🇿 Til": "🇷🇺 Язык",
        "❌ Bekor qilish": "❌ Отмена",
        "✅ Tasdiqlash": "✅ Подтверждение",
        "Ulashish": "Совместное использование",
        "Saqlash": "Сохранять",
        "Tilingiz o'zgartirildi!": "Ваш язык был изменен!",
        "Bo'limni tanglang!": "Выбирайте раздел!",
        'Tilni tanlang!': "Выберите язык!",
        "Post turini tanglang!": "Выберите тип публикации!",
        "Post yaratish bekor qilindi!": "Создание поста отменено!",
        "Post matnini yuboring.": "Отправьте текст поста.",
        "Post rasmini yuboring.": 'Отправьте изображение публикации.',
        "Post gifni yuboring.": "Отправьте gif-пост.",
        "Post videoni yuboring.": "Прикрепите видео поста.",
        "Tugma uchun havolani quyidagicha formatda yuboring.\n"
         "<code>[tugma matni+https://t.me/cleancoder_uz]</code>\n"
         "Tugma qo'shmoqchi bo'lsangiz bir qatordan shu ko'rinishda havolani yuboring.\n"
         "<code>[birinchi matni+https://t.me/cleancoder_uz]</code>\n"
         "<code>[ikkinchi matni+https://t.me/cleancoder_uz]</code>":
        "Отправьте ссылку на кнопку в следующем формате.\n"
         "<code>[текст кнопки+https://t.me/cleancoder_uz]</code>\n"
         "Если вы хотите добавить кнопку, отправьте такую ссылку из одной строки.\n"
         "<code>[первый текст+https://t.me/cleancoder_uz]</code>\n"
         "<code>[второй текст+https://t.me/cleancoder_uz]</code>",
        "Iltimos, rasm yuboring.": "Пожалуйста, пришлите фотографию.",
        "Iltimos, video yuboring.": "Пожалуйста, пришлите видео.",
        "Iltimos, matn yuboring.": 'Пожалуйста, отправьте текст.',
        "Iltimos, GIF yuboring.": "Пожалуйста, пришлите GIF",
        "Iltimos, mos keladigan kontent turini tanlang va yuboring.":
        "Пожалуйста, выберите подходящий тип контента и отправьте его.",
        "Postni o'chirishda xatolik yuz berdi:": "Ошибка удаления сообщения:",
        "Post yaratish bekor qilindi!": "Создание поста отменено!",
        "Postingiz tayyor!\n\n"
            f"Siz uni quyidagi kod orqali istalgan chatda ishlatishingiz mumkin:!":
        "Ваш пост готов!\n\n"
             f"Вы можете использовать его в любом чате с помощью следующего кода:!",
        "Iltimos, tugmalarni quyidagi formatda kiriting:\n"
                                     "<code>[tugma matni+https://t.me/cleancoder_uz]</code>\n"
                                     "<code>[birinchi matni+https://t.me/cleancoder_uz]</code>\n"
                                     "<code>[ikkinchi matni+https://t.me/cleancoder_uz]</code>":
        "Пожалуйста, введите ключи в следующем формате:\n"
        "<code>[текст кнопки+https://t.me/cleancoder_uz]</code>\n"
        "<code>[первый текст+https://t.me/cleancoder_uz]</code>\n"
        "<code>[второй текст+https://t.me/cleancoder_uz]</code>",
        "Xato format:": "Формат ошибки:",
        "Iltimos, <code>[tugma matni+https://t.me/cleancoder_uz]</code> formatida kiriting.":
        "Пожалуйста, введите в формате <code>[текст кнопки+https://t.me/cleancoder_uz]</code>.",
        "Kerakli tugmalardan birini tanlang:": "Выберите одну из необходимых кнопок",
        "Post avval saqlangan.": "Пост ранее сохранен.",
        "Post uchun qisqa nom bering:": "Дайте краткое название поста:",
        "Post nomi bo'sh bo'lishi mumkin emas.": "Название сообщения не может быть пустым.",
        "Post saqlndi.": "Пост сохранен.",
        "Iltimos, post ID yuboring.": "Пожалуйста, пришлите идентификатор сообщения.",
        "Post topilmadi. Iltimos, boshqa post ID yuboring.": "Пост не найдено. Пожалуйста, отправьте другой идентификатор сообщения.",
        "Post topilmadi": "Пост не найдено",
        "Post ID yuborish": "Отправить идентификатор пост",
        "Noto'g'ri post turi. Iltimos, to'g'ri post ID yuboring.": "Неверный тип сообщения. Пожалуйста, отправьте правильный идентификатор сообщения.",
        "Xato": "Ошибка",
        "Post ID noto'g'ri formatda. Iltimos, raqamli post ID yuboring.": "Идентификатор сообщения имеет неверный формат. Пожалуйста, пришлите цифровой идентификатор сообщения.",
        "Sizda saqlangan postlar yoq!": "Вам нравятся сохраненные посты!",
        "Yashirish": "Скрывать",
        "Postni o'chirdingiz!": "Вы удалили пост!",
        "Post ID noto'g'ri formatda!": "Идентификатор сообщения имеет неверный формат!",
        "Xatolik yuz berdi, postni o'chirishda!": "При удалении поста произошла ошибка!",
        "Tilni yangilashdagi xato": "Ошибка обновления языка",

    }
}

def tarjimon_language(text, lang='uz'):
    if lang in translations and text in translations[lang]:
        return translations[lang][text]
    return text