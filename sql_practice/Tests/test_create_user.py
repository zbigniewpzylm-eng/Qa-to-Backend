import pytest
from sql_practice.models import User
from sqlalchemy.exc import IntegrityError

from sqlalchemy import text

def test_db_connection(db_session):
    result = db_session.execute(text("SELECT 1"))

    value = result.scalar()

    assert value == 1    


def test_create_user_persists_to_databa(db_session):
    user = User(
        name="zbigniew",
        email="zbyszek@example.com",
        #age=30,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    saved_user = db_session.get(User, user.id)

    assert saved_user.email == "zbyszek@example.com"

def test_create_user_generates_id(db_session):
    user = User(
        name="zbigniew",
        email="zbyszek@example.com",
        #age=30,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    saved_user = db_session.get(User, user.id)

    assert saved_user.id != None

def test_duplicate_email_rises_err(db_session):
    user = User(
        name="zbigniew",
        email="zbyszek@example.com",
        #age=30,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    user2  = User(
        name="adam",
        email="zbyszek@example.com",
        #age=30,
    )
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()

