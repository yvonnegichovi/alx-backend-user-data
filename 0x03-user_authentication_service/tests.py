#!/usr/bin/env python3
"""
Tests for app.py
"""


import unittest
from app import app
from auth import Auth
from unittest.mock import patch


class AppTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test client
        """
        self.client = app.test_client()
        self.client.testing = True

    @patch.object(Auth, 'register_user')
    def test_register_user_success(self, mock_register_user):
        """
        Test user registration success
        """
        mock_register_user.return_value = type("user", (object,), {"email": "testuser@example.com", "password": "testpassword"})
        response = self.client.post('/users', data={'email': 'testuser@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'email': 'testuser@example.com', 'message': 'user created'})

    @patch.object(Auth, 'register_user')
    def test_register_user_failure(self, mock_register_user):
        """
        Test user registration failure
        """
        mock_register_user.side_effect = ValueError()
        response = self.client.post('/users', data={'email': 'testuser@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {'message': 'email already registered'})

    @patch.object(Auth, 'valid_login', return_value=True)
    @patch.object(Auth, 'create_session', return_value='sessionid123')
    def test_login_success(self, mock_valid_login, mock_create_session):
        """
        Test login success
        """
        response = self.client.post('/sessions', data={'email': 'testuser@example.com', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'email': 'testuser@example.com', 'message': 'logged in'})
        self.assertIn('sessionid123', response.headers.get('Set-Cookie'))

    @patch.object(Auth, 'valid_login', return_value=False)
    def test_login_failure(self, mock_valid_login):
        """
        Test login failure
        """
        response = self.client.post('/sessions', data={'email': 'testuser@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)

    @patch.object(Auth, 'get_user_from_session_id', return_value=None)
    def test_logout_no_session(self, mock_get_user_from_session_id):
        """
        Test logout with no valid session
        """
        response = self.client.delete('/sessions')
        self.assertEqual(response.status_code, 403)

    @patch.object(Auth, 'get_user_from_session_id', return_value=type('User', (object,), {'id': 1})())
    @patch.object(Auth, 'destroy_session')
    def test_logout_success(self, mock_get_user_from_session_id, mock_destroy_session):
        """
        Test logout success
        """
        with self.client as client:
            client.set_cookie('localhost', 'session_id', 'sessionid123')
            response = client.delete('/sessions')
            self.assertEqual(response.status_code, 302)  # redirect status code
            self.assertEqual(response.location, 'http://localhost/')

    @patch.object(Auth, 'get_user_from_session_id', return_value=None)
    def test_profile_no_session(self, mock_get_user_from_session_id):
        """
        Test profile access with no valid session
        """
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 403)

    @patch.object(Auth, 'get_user_from_session_id', return_value=type('User', (object,), {'email': 'testuser@example.com'})())
    def test_profile_success(self, mock_get_user_from_session_id):
        """
        Test profile access success
        """
        with self.client as client:
            client.set_cookie('localhost', 'session_id', 'sessionid123')
            response = client.get('/profile')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'email': 'testuser@example.com'})

    @patch.object(Auth, 'get_reset_password_token', side_effect=ValueError())
    def test_get_reset_password_token_failure(self, mock_get_reset_password_token):
        """
        Test get reset password token failure
        """
        response = self.client.post('/reset_password', data={'email': 'unknown@example.com'})
        self.assertEqual(response.status_code, 403)

    @patch.object(Auth, 'get_reset_password_token', return_value='reset_token_123')
    def test_get_reset_password_token_success(self, mock_get_reset_password_token):
        """
        Test get reset password token success
        """
        response = self.client.post('/reset_password', data={'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'email': 'testuser@example.com', 'reset_token': 'reset_token_123'})


if __name__ == '__main__':
    unittest.main()

