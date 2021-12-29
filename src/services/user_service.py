from typing import Optional

from passlib.handlers.sha2_crypt import sha512_crypt as crypto

from data import db_session
from data.user import User


def user_count() -> int:
    with db_session.create_session() as session:
        return session.query(User).count()


def create_account(name: str, email: str, password: str) -> User:
    with db_session.create_session() as session:
        user = User()
        user.email = email
        user.name = name
        user.hash_password = crypto.hash(password, rounds=172_431)

        session.add(user)
        session.commit()

        return user


def login_user(email: str, password: str) -> Optional[User]:
    with db_session.create_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            return user

        if not crypto.verify(password, user.hash_password):
            return None

        return user


def get_user_by_id(user_id: int) -> Optional[User]:
    with db_session.create_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        return user


def get_user_by_email(email: str) -> Optional[User]:
    with db_session.create_session() as session:
        user = session.query(User).filter(User.email == email).first()
        return user
