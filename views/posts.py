import os
from typing import Optional

from flask import request, render_template, abort, redirect, url_for
from werkzeug.utils import secure_filename

from db.models import Post, Board
from main import app
from sessions import get_current_user
from upload import allowed_file, UPLOAD_FOLDER

POSTS_PER_PAGE = 10


def handle_post(parent: Optional[Post], board: Board):
    """Handles post form submission.

    :param parent: post that form replies to, or None if it's a top-level post
    :param board: board that post belongs to"""

    # Getting current user
    user = get_current_user()
    if not user or user.is_suspended():
        return

    # Getting form fields
    content = request.form.get('content', '')
    anonymous = request.form.get('anonymous', False)
    image = None

    # Loading image to uploads
    if 'image' in request.files:
        image = secure_filename(request.files['image'].filename)
        if image and allowed_file(image):
            request.files['image'].save(os.path.join(UPLOAD_FOLDER, image))

    # If we have all required fields, then we create the post
    if content:
        Post.create(content=content, image=image, anonymous=anonymous, author=user, parent=parent, board=board)


@app.route('/<board>', methods=['GET', 'POST'])
def view_board(board):
    """Board page with all its top-level posts."""

    board_data = Board.get_or_none(Board.slug == board)
    if not board_data:
        abort(404)

    user = get_current_user()
    if request.method == 'POST' and user:
        handle_post(None, board_data)
        return redirect(url_for('view_board', board=board))
    req = Post.select().join(Board).where((Post.parent.is_null()) & (Post.board.slug == board))
    page_number = request.args.get('page', 1, type=int)
    page_count = req.count() // POSTS_PER_PAGE + 1
    posts = req.order_by(Post.created_at.desc()).paginate(page_number, POSTS_PER_PAGE)
    return render_template('posts.html', user=user, posts=posts, page=page_number, pages=page_count, board=board_data)


@app.route('/<board>/<int:post_id>', methods=['GET', 'POST'])
def view_post(board, post_id):
    """Page to view a specific post and all replies to it."""

    user = get_current_user()
    board_data = Board.get_or_none(Board.slug == board)
    if not board_data:
        abort(404)
    post = Post.select().join(Board).where((Post.id == post_id) & (Post.board.slug == board)).get()
    if not post:
        abort(404)
    page_number = request.args.get('page', 1, type=int)
    page_count = post.comments.count() // POSTS_PER_PAGE + 1
    posts = post.comments.order_by(Post.created_at.desc()).paginate(page_number, POSTS_PER_PAGE)

    if request.method == 'POST' and user:
        handle_post(post, post.board)
        return redirect(url_for('view_post', board=board, post_id=post_id))
    return render_template('posts.html', user=user, post=post, posts=posts, page=page_number, pages=page_count,
                           board=board_data)
