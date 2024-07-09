#!/usr/bin/env python3
"""
auth module for the API
"""

from flask import Flask, request
from typing import List, TypeVar


class Auth:
    """
    Class for all authentication system to be implemented
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns False, path and excluded_paths to be used later
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        returns None, request will be the Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        returns None, request will be the Flask request object
        """
        return None
