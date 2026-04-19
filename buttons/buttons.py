from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

def get_subscribe_buttons():
    keyboard = [
        [InlineKeyboardButton("📢 Kanalga o‘tish", url="https://t.me/dasturlash_va_IT_sohalar")],
        [InlineKeyboardButton("✅ Tekshirdim", callback_data="check_sub")]
    ]

    return InlineKeyboardMarkup(keyboard)


def get_main_buttons():
    keyboard = [
        ["📊 Statistika", "📞 Admin bilan bog‘lanish"]
    ]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)