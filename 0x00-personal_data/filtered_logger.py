#!/usr/bin/env python3
"""
Definition of filter_datum function that returns an obfuscated log message
"""
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Return an obfuscated log message
    Args:
        fields: list of strings indicating fields to obfuscate
        redaction: what the field will be obfuscated
        message: the log line to obfuscate
        separator: character separating the fields
    """
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Class Redacting Formatter
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        redact the message
        Args:
        record (logging.LogRecord): LogRecord instance with message
        Return:
            formatted string
        """
        themessage = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, self.REDACTION, themessage, self.SEPARATOR)

        return redacted


def get_logger() -> logging.Logger:
    """
    Return the logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handle = logging.StreamHandler()

    fieldformatter = RedactingFormatter(PII_FIELDS)

    handle.setFormatter(fieldformatter)
    logger.addHandler(handle)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(user=user,password=passwd, host=host, database=db_name)
    return conn


def main():
    """
    entry point to the code
    """
    database = get_db()
    logger = get_logger()
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(key, value) for key, value in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    database.close()


if __name__ == "__main__":
    main()
