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


def test_update_user_does_not_persists_without_commit_to_database(db_session):
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


def test_update_email_with_existing_value_raises_error(db_session):
    user = User(
        name="zbigniew",
        email="zbyszek@example.com",
        #age=30,
    )
    user2  = User(
        name="adam",
        email="adam@example.com",
        #age=30,
    )
    db_session.add(user)
    db_session.add(user2)
    db_session.commit()
    #db_session.refresh(user)
    #db_session.refresh(user2)
    sessionB = TestSessionLocal()
    saved_user = sessionB.get(User, user.id)
    saved_user.email="adam@example.com"
    

    with pytest.raises(IntegrityError):
        sessionB.commit()
    sessionB.rollback()
        
    sessionB.close()