import re

from flask import redirect, url_for, request, render_template
from db.models import User
from main import app
from sessions import get_current_user, set_current_user, clear_current_user
from util import generate_password_hash


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page for logging in and creating new accounts."""

    # If user is already logged in
    if get_current_user():
        # Then we go to homepage
        return redirect(url_for('index'))

    # Initialising default values for the page
    username = ''
    password = ''
    error = None

    # If the form was submitted
    if request.method == 'POST':
        # We get username and password from form data
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        # If both of them are provided
        if username and password:
            # We try to find the user
            user = User.get_or_none(User.username == username)

            # If the user exists
            if user:
                # And the valid password was entered
                if user.validate_password(password):
                    # We log in
                    set_current_user(user)
                    return redirect(url_for('index'))
                else:
                    error = 'password does not match'
            else:
                # If not, we validate username and password
                if len(password) < 8:
                    error = 'password must be at least 8 characters long'
                elif not re.match(r'^[A-Za-z][A-Za-z0-9_-]+[A-Za-z0-9]$', username):
                    error = 'username is not in valid format'
                else:
                    # And register the user
                    password_hash, password_salt = generate_password_hash(password)
                    user = User.create(username=username, password_hash=password_hash, password_salt=password_salt)
                    set_current_user(user)
                    return redirect(url_for('index'))
        else:
            error = 'please fill in all required fields'
    return render_template('login.html', error=error, username=username, password=password, user=None)


@app.route('/logout')
def logout():
    """Logout route that clears session data."""

    clear_current_user()
    return redirect(url_for('index'))
