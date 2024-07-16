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
            self._db.find_user_by(email=email)
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
