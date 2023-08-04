#   Name: William Sung
#   Description: CS493 Capstone
#                Status Checker
from flask import Flask, render_template, request, session, redirect, url_for

from functools import wraps


def status(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return render_template("denied.html")
    return wrapper


def admin_status(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'admin_logged_in' in session:
            return func(*args, **kwargs)
        return render_template("denied.html")
    return wrapper
