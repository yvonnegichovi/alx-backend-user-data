#!/usr/bin/env python3
"""auth module
"""

import bcrypt


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
