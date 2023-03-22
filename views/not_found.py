from flask import render_template

from main import app
from sessions import get_current_user


@app.errorhandler(404)
def page_not_found(_):
    """Page for handling HTTP 404 Not Found error."""

    return render_template('404.html', user=get_current_user()), 404
