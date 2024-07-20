#!/usr/bin/env python3
"""auth module
"""

import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user
        Args:
            - email: email of the user
            - password: password of the user
        Returns:
            - User: the object
        """
        try:
            DB.find_user_by(email=email)
            raise ValueError("User <{}> already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates credentials
        """
        user = self._db._session.query(User).filter_by(email=email).first()
        if user and bcrypt.checkpw(password.encode('utf-8'),
                                   user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """
        Creates a session and returns a session ID
        """
        user = self._db._session.query(User).filter_by(email=email).first()
        if user:
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id
        return None

    def get_user_from_session_id(self, session_id: str) -> User or None:
        """
        Finds a user by session ID
        """
        user = self._db._session.query(User).filter_by(
                session_id=session_id).first()
        if user is None:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a session
        """
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            if user is not None:
                self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User with the given email does not exists")
        reset_token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates password of a User
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        new_hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=new_hashed_password,
                             reset_token=None)


def _generate_uuid() -> str:
    """
    Generates UUIDs
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """
    Defines passwords
    Args:
        - password: password
    returns:
        - bytes: salted hash of the input password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
