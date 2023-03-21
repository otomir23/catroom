from peewee import Model, CharField, BooleanField, ForeignKeyField

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
    is_admin = BooleanField()

    def validate_password(self, password):
        """Checks if a password matches the user's password.

        :param password: password to verify

        :returns: True if computed hashes match, False if not"""
        return verify_password(password, self.password_hash, self.password_salt)


class Post(BaseModel):
    """A model that represents a post. Post always has text and can have an image attached."""

    content = CharField()
    image = CharField(null=True)
    anonymous = BooleanField()
    author = ForeignKeyField(User, backref='posts')
    parent = ForeignKeyField('self', null=True, backref='comments')


def create_tables():
    """Creates all tables in the database."""

    with db:
        db.create_tables([User, Post])