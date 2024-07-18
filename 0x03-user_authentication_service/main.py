#!/usr/bin/env python3
"""
Main file for testing Auth class methods
"""
from auth import Auth
from db import DB
import bcrypt

def create_test_user(email, password):
    """Helper function to create a test user in the database."""
    auth = Auth()
    return auth.register_user(email, password)

def _hash_password(password: str) -> bytes:
    """
    Hashes a password
    Args:
        - password: password
    returns:
        - bytes: salted hash of the input password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Initialize Auth
auth = Auth()

# Test user registration
email = "testuser@example.com"
password = "testpassword"
try:
    user = auth.register_user(email, password)
    print(f"User {user.email} registered successfully")
except ValueError as e:
    print(e)

# Test valid login
print(f"Login valid: {auth.valid_login(email, password)}")

# Test invalid login
print(f"Login valid: {auth.valid_login(email, 'wrongpassword')}")

# Test session creation
session_id = auth.create_session(email)
print(f"Session ID: {session_id}")

# Test getting user from session ID
user_from_session = auth.get_user_from_session_id(session_id)
if user_from_session:
    print(f"User from session ID: {user_from_session.email}")
else:
    print("No user found with that session ID")

# Test destroying session
auth.destroy_session(user.id)
user_from_session = auth.get_user_from_session_id(session_id)
if user_from_session:
    print("Session destruction failed")
else:
    print("Session destroyed successfully")

# Test password reset token generation
reset_token = auth.get_reset_password_token(email)
print(f"Reset token: {reset_token}")

# Test updating password with reset token
new_password = "newpassword"
try:
    auth.update_password(reset_token, new_password)
    print("Password updated successfully")
except ValueError as e:
    print(e)

# Test login with new password
print(f"Login valid: {auth.valid_login(email, new_password)}")

# Test invalid reset token
try:
    auth.update_password("invalid_reset_token", new_password)
    print("This should not print, token should be invalid")
except ValueError as e:
    print(f"Expected error: {e}")

