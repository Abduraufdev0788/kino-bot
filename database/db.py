from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config.config import DATABASE_URL
from database.models import Base

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
