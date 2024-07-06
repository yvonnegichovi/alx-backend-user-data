#!/usr/bin/env python3
"""
This module returns a log message through regex-ing
"""

from typing import List, Tuple
import logging
import mysql.connector
from mysql.connector import connection
import os
import re

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes the variables
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        formats the records
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns a log message obfuscated
    Args:
        - fields - a list of strings representing all fields to obsufucate
        - redaction - a string representing by what the field will be obfuscate
        - message - a string representing the log line
        -- separator - a string representing by which character is seperating
                      all fields in the log line(message)
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m:
                  m.group(0).split('=')[0] + '=' + redaction, message)


def get_logger() -> logging.Logger:
    """
    returns a logging.Logger
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """Connects to the MySQL database and returns the connection object."""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_PASSWORD", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    conn = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    return conn


def main():
    """
    reads and filters data
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()

    for row in cursor:
        msg = f"name={row[0]}; email={row[1]}; phone={row[2]}; ssn={row[3]};
              password={row[4]}; ip={row[5]}; last_login={row[6]};
              user_agent={row[7]};"
        logger.info(msg)

    cursor.close()
    db.close()
