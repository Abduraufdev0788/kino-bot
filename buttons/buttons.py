from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from config.config import CHANNELS

def get_subscribe_buttons():
    keyboard = []
    
    for i, channel in enumerate(CHANNELS, 1):
        # Username orqali URL yaratish (masalan: @kanal -> dasturlash_va_IT_sohalar)
        url = f"https://t.me/{channel.replace('@', '')}"
        keyboard.append([InlineKeyboardButton(f"📢 {i}-kanalga o‘tish", url=url)])
        
    keyboard.append([InlineKeyboardButton("✅ Tekshirdim", callback_data="check_sub")])

    return InlineKeyboardMarkup(keyboard)


def get_main_buttons(is_admin=False):
    keyboard = [
        ["📊 Statistika", "📞 Admin bilan bog‘lanish"],
        ["🎬 Kino kodlari", "💰 Reklama yuborish"]
    ]
    
    if is_admin:
        keyboard.append(["📣 Reklama joylash", "➕ Kino qo'shish"])
        keyboard.append(["🗑 Kino o'chirish"])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)