#!/usr/bin/env python3
"""
A basic Flask app
"""

from auth import Auth
from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """
    Returns a JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """
    Implements the end-point to register a user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    Implements login
    Contains data from email and password
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        response = make_response(jsonify({"email": email,
                                         "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Routes handles logout
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        return jsonify({"error": "Forbidden"}), 403
    user = None
    try:
        user = auth._db.find_user_by(session_id=session_id)
    except NoResultFound:
        return jsonify({"error": "Forbidden"}), 403
    if user:
        auth._db.destroy_session(user.id)
        return redirect('/')
    else:
        return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
