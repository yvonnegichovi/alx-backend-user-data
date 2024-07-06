#!/usr/bin/env python3
"""
This module returns a log message through regex-ing
"""

from typing import List
import logging
import re


import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
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
