from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from config.config import YOUTUBE_CHANNEL

def get_subscribe_buttons(unjoined_channels: list = None):
    keyboard = []
    
    if unjoined_channels:
        for i, channel in enumerate(unjoined_channels, 1):
            # Username orqali URL yaratish (masalan: @kanal -> dasturlash_va_IT_sohalar)
            url = f"https://t.me/{channel.replace('@', '')}"
            keyboard.append([InlineKeyboardButton(f"📢 {i}-kanalga o‘tish", url=url)])
            
    if YOUTUBE_CHANNEL:
        keyboard.append([InlineKeyboardButton("▶️ YouTube kanaliga obuna bo'lish", url=YOUTUBE_CHANNEL)])
        
    keyboard.append([InlineKeyboardButton("✅ Tekshirdim", callback_data="check_sub")])

    return InlineKeyboardMarkup(keyboard)


def get_main_buttons(is_admin=False):
    keyboard = [
        ["📊 Statistika", "📞 Admin bilan bog‘lanish"],
        ["🎬 Kino kodlari", "💰 Reklama yuborish"]
    ]
    
    if is_admin:
        keyboard.append(["📣 Reklama joylash", "➕ Kino qo'shish"])
        keyboard.append(["🗑 Kino o'chirish", "🗄 Baza nusxasi"])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)