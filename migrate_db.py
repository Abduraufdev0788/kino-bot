import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from dotenv import load_dotenv

from database.models import Base, User, Movie

load_dotenv()

# Eski SQLite (yoki hozirgi ishlagan) bazasi URL-si. Misol: sqlite+aiosqlite:///kino.db
OLD_DATABASE_URL = os.getenv("OLD_DATABASE_URL", "sqlite+aiosqlite:///kino.db") 

# Yangi MySQL bazasi URL-si. Misol: mysql+aiomysql://root:password@localhost/kino_bot
NEW_DATABASE_URL = os.getenv("DATABASE_URL") 

if not NEW_DATABASE_URL or "mysql" not in NEW_DATABASE_URL:
    print("XATOLIK: .env dagi DATABASE_URL mysql ga ulanmagan.")
    exit(1)

async def migrate():
    print(f"Eski baza: {OLD_DATABASE_URL}")
    print(f"Yangi baza: {NEW_DATABASE_URL}")

    # Eski baza uchun engine
    old_engine = create_async_engine(OLD_DATABASE_URL, echo=False)
    old_session = sessionmaker(old_engine, class_=AsyncSession, expire_on_commit=False)

    # Yangi MySQL baza uchun engine
    new_engine = create_async_engine(NEW_DATABASE_URL, echo=False)
    new_session = sessionmaker(new_engine, class_=AsyncSession, expire_on_commit=False)

    # Yangi bazada jadvallarni yaratish
    async with new_engine.begin() as conn:
        print("Yangi bazada jadvallar yaratilmoqda...")
        await conn.run_sync(Base.metadata.create_all)

    # Ma'lumotlarni ko'chirish
    async with old_session() as old_s, new_session() as new_s:
        # Users
        print("Foydalanuvchilarni (users) o'qib olyapmiz...")
        result = await old_s.execute(select(User))
        old_users = result.scalars().all()
        
        print(f"Jami {len(old_users)} foydalanuvchi topildi. MySQL'ga yozilmoqda...")
        for u in old_users:
            new_u = User(
                id=u.id, 
                chat_id=u.chat_id, 
                full_name=u.full_name, 
                is_premium=u.is_premium, 
                joined_at=u.joined_at
            )
            # MySQL da allaqachon bo'lsa xatolik bermasligi uchun tekshiramiz yoki to'g'ridan to'g'ri qo'shamiz (merge)
            await new_s.merge(new_u)
        
        await new_s.commit()
        print("Foydalanuvchilar ko'chirildi!")

        # Movies
        print("Kinolarni (movies) o'qib olyapmiz...")
        result = await old_s.execute(select(Movie))
        old_movies = result.scalars().all()

        print(f"Jami {len(old_movies)} kino topildi. MySQL'ga yozilmoqda...")
        for m in old_movies:
            new_m = Movie(
                id=m.id,
                code=m.code,
                title=m.title,
                description=m.description,
                file_id=m.file_id,
                views=m.views,
                created_at=m.created_at
            )
            await new_s.merge(new_m)
            
        await new_s.commit()
        print("Kinolar ko'chirildi!")
        
    print("Migratsiya muvaffaqiyatli yakunlandi!")

if __name__ == "__main__":
    asyncio.run(migrate())
