import pytest
from sql_practice.models import User
from sqlalchemy.exc import IntegrityError, NoResultFound
from conftest import TestSessionLocal


from sqlalchemy import text


def test_delete_user(db_session):
    user = User(
        name="zbigniew",
        email="zbyszek@example.com",
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    db_session.delete(user)
    db_session.commit()

    session_b = TestSessionLocal()

    check_user = session_b.get(User, user.id)

    assert check_user is None
