from telegram import Update
from telegram.ext import ContextTypes
import requests
import httpx
from config.config import Url
from buttons.buttons import get_subscribe_buttons, get_main_buttons
from check_sub.check_sub import check_sub

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    full_name = update.effective_user.full_name
    is_premium = update.effective_user.is_premium

    params = {
        "chat_id": chat_id,
        "full_name": full_name,
        "is_premium": bool(is_premium)
    }

    requests.post(f"{Url}/users/user-create/", json=params)


    if not check_sub(chat_id):
        text = f"""🎬 Assalomu alaykum, {full_name} xush kelibsiz!

Bu bot orqali siz istalgan kinoni maxsus kod orqali topishingiz mumkin 📺

📌 Qanday ishlaydi?
1️⃣ Avval kanalimizga obuna bo‘ling  
👉 https://t.me/dasturlash_va_IT_sohalar  

2️⃣ So‘ng kino kodini yuboring  
3️⃣ Bot sizga kinoni taqdim etadi ✅  

🔍 Masalan: KINO123

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

    await update.message.reply_text(text, reply_markup=get_main_buttons())


async def check_subscription_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.from_user.id

    if check_sub(chat_id):
        await query.message.edit_text("✅ Rahmat! Endi kino kodini yuboring 🎬")
    else:
        await query.answer("❌ Hali ham a’zo emassiz!", show_alert=True)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    code = update.message.text.strip()

    # ❌ a’zo emas
    if not check_sub(chat_id):
        await update.message.reply_text(
            "❌ Avval kanalga a’zo bo‘ling!",
            reply_markup=get_subscribe_buttons()
        )
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{Url}/movies/{code}")

    print(response.status_code)
    print(response.text)

    if response.status_code == 404:
        await update.message.reply_text("❌ Bunday kino mavjud emas")
        return

    data = response.json()

    await update.message.reply_video(
        video=data["file_id"],
        caption=f"🎬 {data['title']}\n\n{data['description']}"
    )


async def handle_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    async with httpx.AsyncClient() as client:
        res = await client.get(f"{Url}/movies/stats")

    data = res.json()
    print(res.status_code)
    print(res.text)


    text = f"""
📊 Statistika:

👥 Userlar: {data['users']}
🎬 Kinolar: {data['movies']}
🔥 Eng mashhur: {data['top_movie']}
👁 Ko‘rishlar: {data['views']}
"""

    await update.message.reply_text(text)


async def contact_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📞 Admin bilan bog‘lanish:\n👉 @Abdurauf_Nasrullayev"
    )