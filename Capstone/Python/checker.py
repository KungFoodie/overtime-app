#   Name: William Sung
#   Description: CS493 Capstone
#                Status Checker
from flask import session

from functools import wraps


def status(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return 'Access Denied'
    return wrapper

