import pytest
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.database.models import Wallet
from tests.constants import WALLET_DATA, WALLET_DATA_AFTER_PUT


def create_db_session():
    username = settings.postgres.user
    password = settings.postgres.password
    port = settings.postgres.port
    db_name = settings.postgres.db_name
    host = "localhost"

    db_engine = "postgresql+psycopg2"
    url = f"{db_engine}://{username}:{password}@{host}:{port}/{db_name}"

    engine = create_engine(url=url)
    session_factory = sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )
    return session_factory()


@pytest.fixture(scope="session", autouse=True)
def drop_data_from_db():
    """Удаление тестового кошелька в случае его существования после тестов"""
    yield

    stmt_1 = delete(Wallet).filter_by(**WALLET_DATA)
    stmt_2 = delete(Wallet).filter_by(**WALLET_DATA_AFTER_PUT)

    with create_db_session() as session:
        session.execute(stmt_1)
        session.execute(stmt_2)
        session.commit()
