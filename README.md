# Kino Bot 🎬

Ushbu loyiha Telegram foydalanuvchilariga maxsus kodlar orqali kinolarni topib beruvchi zamonaviy, avtomatlashtirilgan va tezkor bot hisoblanadi. Bot to'g'ridan-to'g'ri PostgreSQL ma'lumotlar bazasiga ulangan bo'lib, o'zida keng qamrovli admin paneli va statisika tizimini jamlagan.

## 🚀 Asosiy Imkoniyatlar

- **Kino Qidiruv tizimi:** Foydalanuvchilar qisqa kod orqali (masalan: `123`) bazadan kinolarni tezkor izlab topishlari mumkin. Har bir qidiruv kinoning ko'rilishlar sonini (views) avtomatik oshirib boradi.
- **Majburiy A'zolik (Check Sub):** Botdan foydalanish uchun foydalanuvchilar ko'rsatilgan homiy kanalga obuna bo'lishlari shart. Obuna tekshiruvi doimiy ravishda ishlaydi.
- **Admin Panel:** Faqat ruxsat berilgan admin (yoki adminlar) uchun maxsus menyu. Admin to'g'ridan-to'g'ri bot orqali yangi kinolarni kod, rasm/video va tavsiflari bilan bazaga qo'sha oladi va mavjud kinolarni tahrirlay oladi.
- **Ommaviy Xabarnoma (Broadcast):** Barcha bot foydalanuvchilariga bir vaqtning o'zida reklama yoki e'lon tarqatish xususiyati. Xabarlar (video, rasm, audio, matn) qanday yuborilsa, shunday original ko'rinishda foydalanuvchilarga yetib boradi. Spam blokirovkasidan qochish uchun xavfsiz (sleep) funksiyasi qilingan.
- **Dinamik Statistika:** Bot o'zida qancha aktiv foydalanuvchi borligi, nechta kino joylanganligi, kinolarning umumiy ko'rilishlar soni va bazadagi eng mashhur (ko'p ko'rilgan) kinoni doimiy hisoblab ko'rsata oladi.
- **Asinxron Arxitektura:** Botning ma'lumotlar bazasi bilan aloqasi `SQLAlchemy` va `asyncpg` yordamida to'liq asinxron qilingan. Bu orqali minglab foydalanuvchilar bir vaqtda so'rov yuborganda ham bot qotib qolmasdan o'ta tez ishlashda davom etadi.

## 🛠 Texnologiyalar

- **Python 3.12+**
- **python-telegram-bot (v20+)** - Bot API va mantiqiy qismi uchun
- **SQLAlchemy 2.0 (Async)** - Ma'lumotlar bazasi bilan ishlash (ORM) uchun
- **PostgreSQL (asyncpg)** - Asosiy relyatsion ma'lumotlar bazasi sifatida
- **python-dotenv** - Maxfiy kalitlar va muhit o'zgaruvchilarini xavfsiz boshqarish uchun

## ⚙️ Loyihani Ishga Tushirish (Deploy)

### 1. Talablar
Kompyuteringizda yoki serveringizda **Python** va **PostgreSQL** o'rnatilgan hamda ishlayotgan bo'lishi kerak.
PostgreSQL ichida bot uchun qandaydir bo'sh ma'lumotlar bazasi (masalan, `kinobot`) yaratilgan bo'lishi shart.

### 2. Loyihani yuklab olish va o'rnatish
```bash
# Loyiha papkasiga kiring
cd kino-bot

# Virtual muhit yarating
python3 -m venv venv

# Virtual muhitni faollashtiring (Linux/Mac uchun)
source venv/bin/activate
# Windows uchun: venv\Scripts\activate

# Kerakli kutubxonalarni o'rnating
pip install -r requirements.txt
```

### 3. Sozlamalar (.env fayli)
Loyiha papkasidagi `.env` faylini ochib, o'z ma'lumotlaringizni kiriting:

```env
TOKEN = SIZNING_BOT_TOKENINGIZ
DATABASE_URL = postgresql+asyncpg://foydalanuvchi_nomi:parolingiz@localhost:5432/baza_nomi
CHANNEL_ID = @kanal_usernami
ADMIN_ID = 1234567890
```

### 4. Botni ishga tushirish
Barcha sozlamalar to'g'ri bo'lgach, botni quyidagi buyruq bilan ishga tushiring:
```bash
python main.py
```
*Eslatma: Bot birinchi marta ishga tushganida, u avtomatik ravishda orqa fonda PostgreSQL da barcha kerakli jadvallarni (User va Movie) yaratib oladi. Qo'shimcha SQL so'rovlar yozish shart emas.*

---
**Muallif:** [Abdurauf_Nasrullayev](https://t.me/Abdurauf_Nasrullayev)
