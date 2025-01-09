from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


class DB_Helper:
    """Класс для работы с базой данных"""

    def __init__(self, url, echo=False):
        self.url = url
        self.engine = create_async_engine(
            url=self.url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    async def get_session(self):
        """Создание сессии"""
        async with self.session_factory() as session:
            yield session


db_helper = DB_Helper(
    url=settings.postgres.url,
    echo=True,
)
AsyncSessionDep = Annotated[AsyncSession, Depends(db_helper.get_session)]
