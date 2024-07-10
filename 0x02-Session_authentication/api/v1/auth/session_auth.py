#!/usr/bin/env python3
"""
Contains a class SessionAuth
"""

from .auth import Auth


class SessionAuth(Auth):
    """
    creates a new authentication mechanism:
        - validate if everything inherits correctly without any overloading
        - alidate the switch by using environment variables
    """
    pass
