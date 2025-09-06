from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

try:
    from .config import settings
except ImportError:
    from config import settings

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# 👇 Вот это добавляем
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

