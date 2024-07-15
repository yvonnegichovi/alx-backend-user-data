```markdown
# 0x03. User Authentication Service

## Description
This project involves creating a user authentication service using Flask, SQLAlchemy, and bcrypt. The purpose is to build a custom authentication mechanism to understand its inner workings.

## Learning Objectives
By the end of this project, you should be able to explain:
- How to declare API routes in a Flask app
- How to get and set cookies
- How to retrieve request form data
- How to return various HTTP status codes

## Requirements
- All code will be interpreted/compiled on Ubuntu 18.04 LTS using Python 3.7
- Follow PEP 8 style guidelines
- Use SQLAlchemy 1.3.x
- Code should have comprehensive documentation
- All functions should be type-annotated
- Flask app should interact with the Auth class only, not directly with the DB

## Setup
Install the required packages:
```bash
pip3 install bcrypt
```

## Tasks

### Task 0: User model
Create a SQLAlchemy model named `User` for a table `users` with the following attributes:
- `id`: integer primary key
- `email`: non-nullable string
- `hashed_password`: non-nullable string
- `session_id`: nullable string
- `reset_token`: nullable string

### Task 1: Create user
Complete the `DB` class to implement the `add_user` method, which takes `email` and `hashed_password` as arguments and returns a `User` object.

### Task 2: Find user
Implement the `DB.find_user_by` method to return the first user found by filtering the users table with the given arguments. Raise `NoResultFound` or `InvalidRequestError` when appropriate.

### Task 3: Update user
Implement the `DB.update_user` method to update user attributes and commit changes to the database. Raise `ValueError` if the attribute is invalid.

### Task 4: Hash password
Define a `_hash_password` method that returns a salted hash of the input password using `bcrypt.hashpw`.

### Task 5: Register user
Implement the `Auth.register_user` method that registers a user if the email does not already exist, hashes the password, and saves the user to the database.

### Task 6: Basic Flask app
Set up a basic Flask app with a single route (`/`) that returns `{"message": "Bienvenue"}`.

### Task 7: Register user endpoint
Create a `POST /users` route to register a user. Return appropriate JSON responses based on whether the user is successfully registered or already exists.

### Task 8: Credentials validation
Implement the `Auth.valid_login` method to validate user credentials using `bcrypt.checkpw`.

### Task 9: Generate UUIDs
Implement a `_generate_uuid` function that returns a string representation of a new UUID.

### Task 10: Get session ID
Implement the `Auth.create_session` method to generate a new session ID for a user and store it in the database.

### Task 11: Log in
Implement a login function for the `POST /sessions` route. Set the session ID as a cookie on successful login and return a JSON payload.

## Usage
To run the Flask app:
```bash
python3 app.py
```

## Project Structure
```
.
├── README.md
├── app.py
├── auth.py
├── db.py
└── user.py
```

## Authors
- Your Name [Your GitHub Profile]
```
