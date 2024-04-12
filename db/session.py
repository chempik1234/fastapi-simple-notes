from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, scoped_session
from core.config import settings

engine = create_engine(settings.POSTGRES_DATABASE_URL, echo=True)  # SQLALCHEMY_DATABASE_URL
SessionLocal = sessionmaker(engine, expire_on_commit=False, future=True)
# sync_engine = create_engine(settings.POSTGRES_DATABASE_URL, echo=True)  # SYNC_SQLALCHEMY_DATABASE_URL
# SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


def create_session():
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
