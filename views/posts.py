import os
from typing import Optional

from flask import request, render_template, abort
from werkzeug.utils import secure_filename

from db.models import Post
from main import app
from sessions import get_current_user
from upload import allowed_file, UPLOAD_FOLDER


def handle_post(parent: Optional[Post]):
    """Handles post form submission.

    :param parent: post that form replies to, or None if"""

    # Getting current user
    user = get_current_user()
    if not user:
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
        Post.create(content=content, image=image, anonymous=anonymous, author=user, parent=parent)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Homepage with all top-level posts."""

    user = get_current_user()
    if request.method == 'POST' and user:
        handle_post(None)
    posts = Post.select().where(Post.parent.is_null()).order_by(Post.created_at.desc())
    return render_template('posts.html', user=user, posts=posts)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    """Page to view a specific post and all replies to it."""

    user = get_current_user()
    post = Post.get_or_none(Post.id == post_id)
    if not post:
        abort(404)
    posts = post.comments.order_by(Post.created_at.desc())

    if request.method == 'POST' and user:
        handle_post(post)
    return render_template('posts.html', user=user, post=post, posts=posts)
