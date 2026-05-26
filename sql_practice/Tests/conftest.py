import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from models import User


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    yield session

    session.close()

    Base.metadata.drop_all(bind=engine)


from sqlalchemy import text


def test_db_connection(db_session):
    result = db_session.execute(text("SELECT 1"))

    value = result.scalar()

    assert value == 1    