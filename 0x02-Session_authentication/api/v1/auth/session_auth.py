#!/usr/bin/env python3
"""
Contains a class SessionAuth
"""

from .auth import Auth
import uuid


class SessionAuth(Auth):
    """
    creates a new authentication mechanism:
        - validate if everything inherits correctly without any overloading
        - alidate the switch by using environment variables
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a session ID
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
