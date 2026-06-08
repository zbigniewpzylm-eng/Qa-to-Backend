import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sql_practice.models import Base
from sql_practice.models import User


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    session = TestSessionLocal()

    yield session

    session.close()

    Base.metadata.drop_all(bind=engine)




