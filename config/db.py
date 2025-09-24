from sqlmodel import SQLModel, create_engine

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost/postgres"


def create_pg_engine():
    return create_engine(DATABASE_URL, echo=True)


def create_pg_async_engine():
    return create_async_engine(DATABASE_URL, echo=True)


# Create database tables
async def init_db():
    engine = create_pg_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_pg_async_engine()
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    session = session_maker()
    try:
        yield session  # Hand over the session
    except Exception:
        await session.rollback()  # Rollback on error
        raise
    else:
        await session.commit()  # Commit on success
    finally:
        await session.close()  # Always close
        await engine.dispose()  # Clean up engine
