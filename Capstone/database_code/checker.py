#   Name: William Sung
#   Date: 08/20/2022
#   Description: CS336 Assignment# 10
#                Session status checker
from flask import session

from functools import wraps


def status(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return 'Access Denied'
    return wrapper

