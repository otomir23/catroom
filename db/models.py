import datetime

from peewee import Model, CharField, BooleanField, ForeignKeyField, DateTimeField

from db import db, generate_table_name
from util import verify_password


class BaseModel(Model):
    """A base model that will use our SQLite database."""

    class Meta:
        database = db
        legacy_table_names = False
        table_function = generate_table_name


class User(BaseModel):
    """A model that represents a user."""

    username = CharField()
    password_hash = CharField()
    password_salt = CharField()
    is_admin = BooleanField(default=False)
    suspended_until = DateTimeField(null=True)

    def validate_password(self, password):
        """Checks if a password matches the user's password.

        :param password: password to verify

        :returns: True if computed hashes match, False if not"""
        return verify_password(password, self.password_hash, self.password_salt)

    def is_suspended(self):
        """Checks if the user is suspended.

        :returns: True if user is suspended, False if not"""
        return self.suspended_until and self.suspended_until > datetime.datetime.now()

    def get_formatted_unsuspension_date(self):
        """Returns a formatted date string for the user's unsuspension date."""
        return self.suspended_until.strftime('%d.%m.%Y %H:%M')


class Board(BaseModel):
    """A model that represents a board."""

    name = CharField()
    slug = CharField()


class Post(BaseModel):
    """A model that represents a post. Post always has text and can have an image attached."""

    content = CharField()
    image = CharField(null=True)
    anonymous = BooleanField()
    author = ForeignKeyField(User, backref='posts', on_delete='CASCADE')
    parent = ForeignKeyField('self', null=True, backref='comments', on_delete='CASCADE')
    created_at = DateTimeField(default=datetime.datetime.now)
    board = ForeignKeyField(Board, backref='posts', on_delete='CASCADE')

    def get_formatted_date(self):
        """Returns a formatted date string for the post."""
        return self.created_at.strftime('%d.%m.%Y %H:%M')


def create_tables():
    """Creates all tables in the database."""

    with db:
        db.create_tables([User, Board, Post])
