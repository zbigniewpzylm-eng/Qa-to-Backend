import pytest
from sql_practice.models import User
from sqlalchemy.exc import IntegrityError
from conftest import TestSessionLocal

from sqlalchemy import text

def test_update_user_persists_to_database(db_session):
    user = User(
        name="zbigniew",
        email="zbyszek@example.com",
        #age=30,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    saved_user = db_session.get(User, user.id)
    saved_user.email="darek@odpieczarek.com"
    db_session.commit()
   

    sessionB = TestSessionLocal()
    check_user = sessionB.get(User, user.id)
    assert check_user.email == "darek@odpieczarek.com"
    sessionB.close()


def test_update_user_does_persists_without_commit_to_database(db_session):
    user = User(
        name="zbigniew",
        email="zbyszek@example.com",
        #age=30,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    saved_user = db_session.get(User, user.id)
    saved_user.email="darek@odpieczarek.com"
    #db_session.commit()
   

    sessionB = TestSessionLocal()
    check_user = sessionB.get(User, user.id)
    assert check_user.email == "zbyszek@example.com"
    sessionB.close()