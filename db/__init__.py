import re
from flask import Flask
from peewee import PostgresqlDatabase

from db.credentials import DatabaseCredentials

# Loading credentials from file
credentials = DatabaseCredentials()

# Creating a database connection
db = PostgresqlDatabase(
    credentials.db_name,
    user=credentials.db_username,
    password=credentials.db_password.get_secret_value(),
    host=credentials.db_host,
    port=credentials.db_port,
)


def setup_db_connection(app: Flask):
    """Adds middleware that connects to db on each request and disconnects after.

    :param app: flask app to add middleware to"""

    # Connect to db before each request
    @app.before_request
    def _db_connect():
        db.connect()

    # Disconnect from db after each request
    @app.teardown_request
    def _db_close(*_):
        if not db.is_closed():
            db.close()


def generate_table_name(model):
    """Generates a table name for a model.

    :param model: model to generate a table name for

    :returns: table name for the model"""

    # Splitting the model name into words using regex made for pascal case
    words = re.split(r'(?<=[A-Z])(?=[A-Z][a-z])|(?<=[^A-Z])(?=[A-Z])|(?<=[A-Za-z])(?=[^A-Za-z])', model.__name__)
    # Joining the words with underscores
    singular = '_'.join(words).lower()
    # Adding an 's' to the end of the name (or 'es' if the name ends with 's')
    plural = singular + 'es' if singular.endswith('s') else singular + 's'

    return plural
