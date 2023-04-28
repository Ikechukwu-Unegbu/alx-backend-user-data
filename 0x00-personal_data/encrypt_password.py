#!/usr/bin/env python3
"""
Encrypt password task file
"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """
    Returns already hashed password
    Args:
        password (str): plain text password yet to be hashed
    """
    plaintext = password.encode()
    hashed = hashpw(plaintext, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Verify that password matches hash
    Args:
        hashed_password (bytes): hashed password
        password (str): plain text unhashed
    Return:
        bool
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

