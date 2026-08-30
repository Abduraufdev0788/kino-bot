from telegram import Update
from telegram.ext import ContextTypes
from buttons.buttons import get_subscribe_buttons, get_main_buttons
from check_sub.check_sub import check_sub
from database.db import async_session
from database.models import User, Movie
from sqlalchemy import select, func
from config.config import ADMIN_ID
from buttons.buttons import get_subscribe_buttons, get_main_buttons
from check_sub.check_sub import check_sub

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    full_name = update.effective_user.full_name
    is_premium = bool(update.effective_user.is_premium)

    is_new_user = False
    total_users = 0

    try:
        async with async_session() as session:
            # Check if user exists
            stmt = select(User).where(User.chat_id == chat_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            
            if not user:
                try:
                    new_user = User(chat_id=chat_id, full_name=full_name, is_premium=is_premium)
                    session.add(new_user)
                    await session.commit()
                    is_new_user = True
                    total_users = await session.scalar(select(func.count(User.id)))
                except Exception as e:
                    await session.rollback()
                    print(f"Yangi userni saqlashda xatolik: {e}")
    except Exception as e:
        print(f"Start db xatolik: {e}")

    if is_new_user:
        # Adminga xabar yuborish (Baza band bo'lmasligi uchun sessiondan tashqarida)
        try:
            admin_text = f"🆕 Yangi foydalanuvchi qo'shildi!\n\n👤 Ism-familiya: {full_name}\n🆔 ID: {chat_id}\n📊 U botning {total_users}-foydalanuvchisi bo'ldi."
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text)
        except Exception:
            pass


    if not await check_sub(chat_id, context):
        text = f"""🎬 Assalomu alaykum, {full_name} xush kelibsiz!

Bu bot orqali siz istalgan kinoni maxsus kod orqali topishingiz mumkin 📺

📌 Qanday ishlaydi?
1️⃣ Avval botdan foydalanish uchun quyidagi barcha kanallarga obuna bo‘ling.
2️⃣ So‘ng kino kodini yuboring  
3️⃣ Bot sizga kinoni taqdim etadi ✅  

🔍 Masalan: 123

🚀 Marhamat, foydalanishni boshlang!
"""
        await update.message.reply_text(
            text,
            reply_markup=get_subscribe_buttons()
        )
        return

    text = f"""🎬 Assalomu alaykum, {full_name} xush kelibsiz!

Bu bot orqali siz istalgan kinoni maxsus kod orqali topishingiz mumkin 📺

📌 Qanday ishlaydi?

1️⃣Kino kodini yuboring  
2️⃣ Bot sizga kinoni taqdim etadi ✅  

🔍 Masalan: 123

🚀 Marhamat, foydalanishni boshlang!
"""

    await update.message.reply_text(text, reply_markup=get_main_buttons(is_admin=str(chat_id) == str(ADMIN_ID)))


async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.from_user.id

    if await check_sub(chat_id, context):
        await query.answer()
        await query.message.edit_text("✅ Rahmat! Endi kino kodini yuboring 🎬")
    else:
        await query.answer("❌ Hali hamma kanallarga a’zo bo'lmadingiz!", show_alert=True)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    code = update.message.text.strip()

    # ❌ a’zo emas
    if not await check_sub(chat_id, context):
        await update.message.reply_text(
            "❌ Avval barcha kanallarga a’zo bo‘ling!",
            reply_markup=get_subscribe_buttons()
        )
        return

    movie_found = False
    try:
        async with async_session() as session:
            stmt = select(Movie).where(Movie.code == code)
            result = await session.execute(stmt)
            movie = result.scalars().first()

            if movie:
                movie_found = True
                movie.views += 1
                file_id = movie.file_id
                title = movie.title
                description = movie.description
                await session.commit()
    except Exception as e:
        print(f"Kino qidirishda DB xatoligi: {e}")
        await update.message.reply_text("❌ Tizimda xatolik yuz berdi. Iltimos keyinroq urinib ko'ring.")
        return

    if not movie_found:
        await update.message.reply_text("❌ Bunday kino mavjud emas")
        return

    await update.message.reply_video(
        video=file_id,
        caption=f"🎬 {title}\n\n{description}"
    )


async def handle_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text("⏳ Statistika olinmoqda...")

    async with async_session() as session:
        users_count = await session.scalar(select(func.count(User.id))) or 0
        movies_count = await session.scalar(select(func.count(Movie.id))) or 0
        total_views = await session.scalar(select(func.sum(Movie.views))) or 0
        
        stmt = select(Movie).order_by(Movie.views.desc()).limit(1)
        result = await session.execute(stmt)
        top_movie_obj = result.scalar_one_or_none()
        
        top_movie = top_movie_obj.title if top_movie_obj else "Yo'q"

    text = f"""
📊 Statistika:

👥 Userlar: {users_count}
🎬 Kinolar: {movies_count}
🔥 Eng mashhur: {top_movie}
👁 Ko‘rishlar: {total_views}
"""

    await message.edit_text(text)


async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Admin bilan bog‘lanish:\n👉 @Abdurauf_Nasrullayev"
    )

async def movie_codes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Barcha kino kodlarini bizning asosiy kanalimizdan topishingiz mumkin:\n👉 https://t.me/dasturlash_va_IT_sohalar"
    )

async def advertise_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📢 <b>Reklama bo'yicha bog'lanish</b>\n\n"
        "Kanal yoki botda reklama joylashtirish uchun quyidagi ma'lumotlar orqali bog'lanishingiz mumkin:\n\n"
        "👤 <b>Admin:</b> Abdurauf Nasrullayev\n"
        "📱 <b>Telefon:</b> +998 95 289 87 88\n"
        "💬 <b>Telegram:</b> @Abdurauf_Nasrullayev\n\n"
        "💳 <b>Karta raqami:</b>\n"
        "<code>9860 1901 0971 8980</code>\n"
        "👤 <b>Karta egasi:</b> Abdurauf Nasrullayev\n\n"
        "✅ To'lov qilgandan so'ng chekni adminga yuboring.",
        parse_mode="HTML"
    )