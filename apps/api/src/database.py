from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

try:
    # когда запускается внутри пакета (FastAPI)
    from .config import settings
except ImportError:
    # когда запускается Alembic напрямую
    from config import settings

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
