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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a Uset instance based on a cookie value
        """
