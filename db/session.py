from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from core.config import settings

engine = create_async_engine(settings.POSTGRES_DATABASE_URL, echo=True)  # SQLALCHEMY_DATABASE_URL
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
# sync_engine = create_engine(settings.POSTGRES_DATABASE_URL, echo=True)  # SYNC_SQLALCHEMY_DATABASE_URL
# SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
