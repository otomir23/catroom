from flask import render_template, request

from db.models import Board
from sessions import get_current_user
from main import app


@app.route('/', methods=['GET', 'POST'])
def index():
    """Homepage with all boards."""
    user = get_current_user()
    if request.method == 'POST' and user and user.is_admin:
        Board.create(name=request.form.get('name', 'Unnamed Board'), slug=request.form.get('slug', 'meow'))
    return render_template('index.html', user=user, boards=Board.select())
