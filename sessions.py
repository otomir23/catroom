from typing import Optional
from flask import session
from db.models import User


def set_current_user(user: User):
    """Sets the current user in the session.

    :param user: user to set as current"""
    session['logged_in'] = True
    session['user_id'] = user.id


def get_current_user() -> Optional[User]:
    """Gets the current user from the session.

    :returns: current user or None if no user is logged in"""
    if session.get('logged_in', False):
        return User.get_or_none(User.id == session.get('user_id'))
    return None


def clear_current_user():
    """Clears the current user from the session."""
    session.clear()
