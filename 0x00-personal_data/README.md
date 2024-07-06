# 0x00. Personal Data

## Back-end Authentication

### Resources

Read or watch:

- [What Is PII, non-PII, and Personal Data?](https://example.com)
- [logging documentation](https://docs.python.org/3/library/logging.html)
- [bcrypt package](https://pypi.org/project/bcrypt/)
- [Logging to Files, Setting Levels, and Formatting](https://realpython.com/python-logging/)

### Learning Objectives

By the end of this project, you should be able to explain the following concepts without the help of Google:

- Examples of Personally Identifiable Information (PII)
- How to implement a log filter that will obfuscate PII fields
- How to encrypt a password and check the validity of an input password
- How to authenticate to a database using environment variables

### Requirements

- All your files will be interpreted/compiled on Ubuntu 18.04 LTS using python3 (version 3.7)
- All your files should end with a new line
- The first line of all your files should be exactly `#!/usr/bin/env python3`
- A README.md file, at the root of the folder of the project, is mandatory
- Your code should use the pycodestyle style (version 2.5)
- All your files must be executable
- The length of your files will be tested using `wc`
- All your modules should have a documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
- All your classes should have a documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
- All your functions (inside and outside a class) should have a documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`)
- A documentation is not a simple word; it’s a real sentence explaining the purpose of the module, class, or method (the length of it will be verified)
- All your functions should be type annotated

## Tasks

### 0. Regex-ing

**File**: `filtered_logger.py`

Write a function called `filter_datum` that returns the log message obfuscated:

- **Arguments**:
  - `fields`: A list of strings representing all fields to obfuscate
  - `redaction`: A string representing by what the field will be obfuscated
  - `message`: A string representing the log line
  - `separator`: A string representing the character separating all fields in the log line (message)
- The function should use a regex to replace occurrences of certain field values.
- `filter_datum` should be less than 5 lines long and use `re.sub` to perform the substitution with a single regex.

Example:
```python
filter_datum = __import__('filtered_logger').filter_datum

fields = ["password", "date_of_birth"]
messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))
```

Output:
```
name=egg;email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;
name=bob;email=bob@dylan.com;password=xxx;date_of_birth=xxx;
```

### 1. Log formatter

**File**: `filtered_logger.py`

Copy the following code into `filtered_logger.py` and update the `RedactingFormatter` class:

```python
import logging

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: list):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
```

### 2. Create logger

**File**: `filtered_logger.py`

Implement a `get_logger` function that takes no arguments and returns a `logging.Logger` object.

- The logger should be named "user_data" and only log up to `logging.INFO` level. It should not propagate messages to other loggers. It should have a `StreamHandler` with `RedactingFormatter` as formatter.
- Create a tuple `PII_FIELDS` constant at the root of the module containing the fields from `user_data.csv` that are considered PII. 

### 3. Connect to secure database

**File**: `filtered_logger.py`

Database credentials should NEVER be stored in code or checked into version control. Implement a `get_db` function that returns a connector to the database (`mysql.connector.connection.MySQLConnection` object).

- Use the `os` module to obtain credentials from the environment.
- Use the module `mysql-connector-python` to connect to the MySQL database (`pip3 install mysql-connector-python`).

Example:
```python
import os
import mysql.connector

def get_db() -> mysql.connector.connection.MySQLConnection:
    return mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
```

### 4. Read and filter data

**File**: `filtered_logger.py`

Implement a `main` function that takes no arguments and returns nothing.

- The function will obtain a database connection using `get_db` and retrieve all rows in the `users` table, displaying each row under a filtered format.

### 5. Encrypting passwords

**File**: `encrypt_password.py`

Implement a `hash_password` function that expects one string argument named `password` and returns a salted, hashed password, which is a byte string.

- Use the `bcrypt` package to perform the hashing (`with hashpw`).

### 6. Check valid password

**File**: `encrypt_password.py`

Implement an `is_valid` function that expects 2 arguments and returns a boolean.

- Arguments:
  - `hashed_password`: bytes type
  - `password`: string type
- Use `bcrypt` to validate that the provided password matches the hashed password.

## Repository

- **GitHub repository**: `alx-backend-user-data`
- **Directory**: `0x00-personal_data`

Make sure to follow all the requirements and complete the tasks as specified. Good luck!
