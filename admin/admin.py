from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from state import VIDEO, CODE, TITLE, DESCRIPTION, EDIT_CODE, NEW_DESC, NEW_TITLE, BROADCAST_MSG, DELETE_CODE
from database.db import async_session
from database.models import User, Movie
from sqlalchemy import select
import asyncio

from config.config import ADMIN_ID


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

    async with async_session() as session:
        # Check if movie code already exists
        stmt = select(Movie).where(Movie.code == context.user_data["code"])
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            await update.message.reply_text("❌ Bunday kodli kino allaqachon mavjud. Boshqa kod kiriting.")
            context.user_data.clear()
            return ConversationHandler.END

        new_movie = Movie(
            code=context.user_data["code"],
            file_id=context.user_data["file_id"],
            title=context.user_data["title"],
            description=context.user_data["description"]
        )
        session.add(new_movie)
        await session.commit()

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

    async with async_session() as session:
        stmt = select(Movie).where(Movie.code == code)
        result = await session.execute(stmt)
        movie = result.scalar_one_or_none()

        if movie:
            movie.title = context.user_data["title"]
            movie.description = context.user_data["description"]
            await session.commit()
            await update.message.reply_text("✅ Kino yangilandi!")
        else:
            await update.message.reply_text("❌ Bunday kodli kino topilmadi.")

    context.user_data.clear()
    return ConversationHandler.END


async def delete_movie_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        await update.message.reply_text("❌ Siz admin emassiz")
        return ConversationHandler.END
    await update.message.reply_text("🗑 O'chirmoqchi bo'lgan kino kodini yuboring:")
    return DELETE_CODE

async def delete_movie_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()

    async with async_session() as session:
        stmt = select(Movie).where(Movie.code == code)
        result = await session.execute(stmt)
        movie = result.scalar_one_or_none()

        if movie:
            await session.delete(movie)
            await session.commit()
            await update.message.reply_text(f"✅ {code} kodli kino muvaffaqiyatli o'chirildi!")
        else:
            await update.message.reply_text("❌ Bunday kodli kino topilmadi.")

    return ConversationHandler.END


async def broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != int(ADMIN_ID):
        await update.message.reply_text("❌ Siz admin emassiz")
        return ConversationHandler.END
    await update.message.reply_text("📣 Tarqatmoqchi bo'lgan xabaringizni yuboring (matn, rasm, video, audio va hokazo):")
    return BROADCAST_MSG


async def broadcast_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Xabar tarqatish boshlandi...")
    
    async with async_session() as session:
        try:
            stmt = select(User.chat_id)
            result = await session.execute(stmt)
            users = result.scalars().all()
        except Exception as e:
            await update.message.reply_text(f"❌ Baza bilan aloqada xatolik yuz berdi: {e}")
            return ConversationHandler.END
            
    success = 0
    fail = 0
        
    for chat_id in users:
        if not chat_id:
            continue
            
        try:
            await update.message.copy(chat_id=chat_id)
            success += 1
        except Exception:
            fail += 1
            
        await asyncio.sleep(0.05)
        
    await update.message.reply_text(f"✅ Xabar tarqatish yakunlandi!\n\n📤 Muvaffaqiyatli: {success} ta\n❌ Bloklagan/Xatolik: {fail} ta")
    return ConversationHandler.END
