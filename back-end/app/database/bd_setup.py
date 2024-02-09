""" this file configure setup for connecting with BD """
from contextlib import asynccontextmanager
from sqlmodel import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

from logging import getLogger
import json
import os

# logger
logger = getLogger("vibraphile")
engine: AsyncEngine | None = None


async def test_database_connection():
    """ test the connection at the database """
    try:
        query = text("SELECT 1")
        async with get_session() as session:
            await session.execute(query)
        logger.info("Database connection successful!")
    except Exception as e:
        logger.exception(f"Error connecting to the database: {str(e)}")
        raise


async def init_connection():
    """ initialise the tkconnection at the database """
    if not os.path.exists('app/database/config.json'):
        logger.error("need to have the file config.json in database/."
                     " Answer access from a developper.")
        return
    with open('app/database/config.json') as config_connection:
        connect_info: json = json.load(config_connection)
    DATABASE_URL: str = f'postgresql+asyncpg://{connect_info["user"]}:'\
                        f'{connect_info["password"]}@'\
                        f'{connect_info["host"]}:'\
                        f'{connect_info["port"]}/'\
                        f'{connect_info["database"]}'
    global engine
    engine = create_async_engine(DATABASE_URL,
                                 echo=False,  # Turn True to debug
                                 future=True,
                                 pool_size=20,
                                 max_overflow=20,
                                 pool_recycle=3600)
    await test_database_connection()


@asynccontextmanager
async def get_session() -> AsyncSession:
    """get async_session for transaction

    Returns:
        AsyncSession:

    Yields:
        Iterator[AsyncSession]:
    """
    async_session = sessionmaker(engine, class_=AsyncSession,
                                 expire_on_commit=False)
    async with async_session() as session:
        yield session
