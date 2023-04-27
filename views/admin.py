import datetime

from flask import abort, redirect, url_for, request, render_template

from db.models import Post, User
from sessions import get_current_user
from main import app


@app.route('/<board>/<int:post_id>/delete')
def delete_post(board, post_id):
    """Deletes post with given id."""
    user = get_current_user()
    post = Post.get_or_none(Post.id == post_id)
    if not user or not user.is_admin or not post or post.board.slug != board:
        abort(404)
    post.delete_instance()
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/suspend', methods=['GET', 'POST'])
def suspend_user(user_id):
    """Suspends user with given id."""
    user = get_current_user()
    if not user or not user.is_admin:
        abort(404)
    target = User.get_or_none(User.id == user_id)
    if not target:
        abort(404)
    if request.method == 'POST':
        suspension_period = request.form.get('suspension_period', 3, type=int)
        target.suspended_until = datetime.datetime.now() + datetime.timedelta(days=suspension_period)
        target.save()
        return redirect(url_for('index'))

    return render_template('suspend_user.html', user=user, target=target)


@app.route('/users/<int:user_id>/ban')
def ban_user(user_id):
    """Bans user with given id."""
    user = get_current_user()
    if not user or not user.is_admin:
        abort(404)
    target = User.get_or_none(User.id == user_id)
    if not target:
        abort(404)

    target.delete_instance(recursive=True)
    return redirect(url_for('index'))
