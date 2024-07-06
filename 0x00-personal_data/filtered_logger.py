#!/usr/bin/env python3
"""
This module returns a log message through regex-ing
"""

from typing import List
import re

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Returns a log message obfuscated
    Args:
        - fields - a list of strings representing all fields to obsufucate
        - redaction - a string representing by what the field will be obfuscate
        - message - a string representing the log line
        -- separator - a string representing by which character is seperating
                      all fields in the log line(message)
    """
    return re.sub(pattern, lambda m:
           m.group(0).split('=')[0] + '=' + reduction, message)
