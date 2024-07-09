# 0x01. Basic Authentication

## Back-end Authentication

### Project Information

- **Weight**: 1
- **Project Start**: Jul 8, 2024, 6:00 AM
- **Project End**: Jul 10, 2024, 6:00 AM
- **Checker Release**: Jul 8, 2024, 6:00 PM
- **Auto Review**: Launched at the deadline

### Background Context

In this project, you will learn about the authentication process and implement Basic Authentication on a simple API. Note that in real-world applications, you should use a module or framework for Basic Authentication, like Flask-HTTPAuth in Python-Flask. This project aims to walk you through each step of this mechanism to help you understand it by doing.

### Resources

Read or watch:

- REST API Authentication Mechanisms
- Base64 in Python
- HTTP header Authorization
- Flask
- Base64 - concept

### Learning Objectives

By the end of this project, you should be able to explain the following concepts:

- What authentication means
- What Base64 is
- How to encode a string in Base64
- What Basic Authentication means
- How to send the Authorization header

### Requirements

- **Python Scripts**: 
  - Interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
  - All files should end with a new line
  - The first line of all your files should be exactly `#!/usr/bin/env python3`
  - A `README.md` file at the root of the folder is mandatory
  - Code should use the pycodestyle style (version 2.5)
  - All files must be executable
  - The length of your files will be tested using `wc`
  - All modules should have documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
  - All classes should have documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
  - All functions (inside and outside a class) should have documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`)
  - Documentation should be a real sentence explaining the purpose of the module, class, or method (the length will be verified)

### Tasks

#### 0. Simple-basic-API

**Mandatory**

Download and start your project from [this archive](archive.zip). This archive contains a simple API with one model: User. User data is stored via serialization/deserialization in files.

**Setup and start server:**

```bash
pip3 install -r requirements.txt
API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```

**Use the API:**

```bash
curl "http://0.0.0.0:5000/api/v1/status" -vvv
```

**Repository:**

- GitHub repository: `alx-backend-user-data`
- Directory: `0x01-Basic_authentication`

#### 1. Error handler: Unauthorized

**Mandatory**

- **Edit** `api/v1/app.py`:
  - Add a new error handler for status code 401 with JSON response `{"error": "Unauthorized"}`.
  - Use `jsonify` from Flask.
- **For testing**:
  - Add a new endpoint in `api/v1/views/index.py`: Route: `GET /api/v1/unauthorized`
  - This endpoint must raise a 401 error using `abort`.

**Repository:**

- GitHub repository: `alx-backend-user-data`
- Directory: `0x01-Basic_authentication`
- Files: `api/v1/app.py`, `api/v1/views/index.py`

#### 2. Error handler: Forbidden

**Mandatory**

- **Edit** `api/v1/app.py`:
  - Add a new error handler for status code 403 with JSON response `{"error": "Forbidden"}`.
  - Use `jsonify` from Flask.
- **For testing**:
  - Add a new endpoint in `api/v1/views/index.py`: Route: `GET /api/v1/forbidden`
  - This endpoint must raise a 403 error using `abort`.

**Repository:**

- GitHub repository: `alx-backend-user-data`
- Directory: `0x01-Basic_authentication`
- Files: `api/v1/app.py`, `api/v1/views/index.py`

#### 3. Auth class

**Mandatory**

- **Create a folder** `api/v1/auth`.
- **Create an empty file** `api/v1/auth/__init__.py`.
- **Create the class `Auth`** in the file `api/v1/auth/auth.py`:
  - Import `request` from Flask.
  - Public methods:
    - `def require_auth(self, path: str, excluded_paths: List[str]) -> bool`: returns `False`.
    - `def authorization_header(self, request=None) -> str`: returns `None`.
    - `def current_user(self, request=None) -> TypeVar('User')`: returns `None`.

**Repository:**

- GitHub repository: `alx-backend-user-data`
- Directory: `0x01-Basic_authentication`
- Files: `api/v1/auth`, `api/v1/auth/__init__.py`, `api/v1/auth/auth.py`

#### 4. Define which routes don't need authentication

**Mandatory**

- **Update the method** `def require_auth(self, path: str, excluded_paths: List[str]) -> bool` in `Auth`:
  - Returns `True` if `path` is `None`.
  - Returns `True` if `excluded_paths` is `None` or empty.
  - Returns `False` if `path` is in `excluded_paths`.
  - Ensure method is slash tolerant.

**Repository:**

- GitHub repository: `alx-backend-user-data`
- Directory: `0x01-Basic_authentication`
- Files: `api/v1/auth/auth.py`

#### 5. Request validation!

**Mandatory**

- **Update the method** `def authorization_header(self, request=None) -> str` in `api/v1/auth/auth.py`:
  - Returns `None` if `request` is `None`.
  - Returns `None` if `request` doesn’t contain the header key `Authorization`.
  - Returns the value of the header `Authorization`.
- **Update** `api/v1/app.py`:
  - Create a variable `auth` initialized to `None` after the CORS definition.
  - Load and assign the right instance of authentication to `auth` based on the environment variable `AUTH_TYPE`.
  - Filter each request using Flask method `before_request`:
    - Do nothing if `auth` is `None`.
    - Do nothing if `request.path` is not part of the list `['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']`.
    - Raise error 401 if `auth.authorization_header(request)` returns `None`.
    - Raise error 403 if `auth.current_user(request)` returns `None`.

**Repository:**

- GitHub repository: `alx-backend-user-data`
- Directory: `0x01-Basic_authentication`
- Files: `api/v1/app.py`, `api/v1/auth/auth.py`

#### 6. Basic auth

**Mandatory**

- **Create a class** `BasicAuth` that inherits from `Auth`. Initially, this class will be empty.
- **Update** `api/v1/app.py` to use `BasicAuth` class instead of `Auth` based on the environment variable `AUTH_TYPE`.

**Repository:**

- GitHub repository: `alx-backend-user-data`
- Directory: `0x01-Basic_authentication`
- Files: `api/v1/app.py`, `api/v1/auth/basic_auth.py`

#### 7. Basic - Base64 part

**Mandatory**

- **Add the method** `def extract_base64_authorization_header(self, authorization_header: str) -> str` in `BasicAuth` class:
  - Returns the Base64 part of the Authorization header for a Basic Authentication.
  - Returns `None` if `authorization_header` is `None`, not a string, or doesn’t start with `Basic`.

**Repository:**

- GitHub repository: `alx-backend-user-data`
- Directory: `0x01-Basic_authentication`
- Files: `api/v1/auth/basic_auth.py`

#### 8. Basic - Base64 decode

**Mandatory**

- **Add the method** `def decode_base64_authorization_header(self, base64_authorization_header: str) -> str` in `BasicAuth` class:
  - Returns the decoded value of a Base64 string `base64_authorization_header`.
  - Returns `None` if `base64_authorization_header` is `None`, not a string, or not a valid Base64.

**Repository:**

- GitHub repository: `alx-backend-user-data`
- Directory: `0x01-Basic_authentication`
- Files: `api/v1/auth/basic_auth.py`

#### 9. Basic - User credentials

**Mandatory**

- **Add the method** `def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str)` in `BasicAuth` class:
  - Returns the user email and password from the Base64 decoded value.
  - Returns `None, None` if `decoded
