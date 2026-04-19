from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from state import VIDEO, CODE, TITLE, DESCRIPTION, EDIT_CODE, NEW_DESC, NEW_TITLE
import httpx

from config.config import Url, ADMIN_ID


async def add_movie_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        await update.message.reply_text("❌ Siz admin emassiz")
        return ConversationHandler.END
    await update.message.reply_text("🎬 Videoni yuboring")
    return VIDEO


async def get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video

    context.user_data["file_id"] = video.file_id

    await update.message.reply_text("🔢 Kino kodini yuboring (masalan: KINO123)")
    return CODE


async def get_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["code"] = update.message.text.strip()

    await update.message.reply_text("🎬 Kino nomini yozing")
    return TITLE

async def get_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text

    await update.message.reply_text("📄 Tavsif yozing")
    return DESCRIPTION


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi")
    return ConversationHandler.END



async def save_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["description"] = update.message.text

    data = {
        "code": context.user_data["code"],
        "file_id": context.user_data["file_id"],
        "title": context.user_data["title"],
        "description": context.user_data["description"],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{Url}/movies/", json=data)

    await update.message.reply_text("✅ Kino saqlandi!")

    context.user_data.clear()

    return ConversationHandler.END







async def edit_movie_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        await update.message.reply_text("❌ Siz admin emassiz")
        return ConversationHandler.END
    await update.message.reply_text("✏️ Qaysi kino kodini o‘zgartirmoqchisiz?")
    return EDIT_CODE


async def get_edit_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["code"] = update.message.text.strip()

    await update.message.reply_text("🆕 Yangi nomni yozing")
    return NEW_TITLE


async def get_new_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text

    await update.message.reply_text("📝 Yangi description yozing")
    return NEW_DESC




async def save_updated_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["description"] = update.message.text

    code = context.user_data["code"]

    data = {
        "title": context.user_data["title"],
        "description": context.user_data["description"]
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(f"{Url}/movies/{code}", json=data)

    if response.status_code == 200:
        await update.message.reply_text("✅ Kino yangilandi!")
    else:
        await update.message.reply_text("❌ Xatolik yuz berdi")

    context.user_data.clear()
    return ConversationHandler.END


