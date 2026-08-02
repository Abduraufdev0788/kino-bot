from telegram.ext import ContextTypes
from telegram.error import TelegramError
from config.config import CHANNELS

async def check_sub(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not CHANNELS:
        return True
        
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=chat_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except TelegramError:
            return False
            
    return True