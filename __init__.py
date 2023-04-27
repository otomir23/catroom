from flask import Flask
from pydantic import BaseSettings, SecretStr, Field

from db import setup_db_connection
from db.models import create_tables
from upload import setup_app_uploads


# The app object is created here, so that it can be imported by other modules.
app = Flask(__name__)


class AppConfig(BaseSettings):
    """Application configuration."""
    SECRET_KEY: SecretStr = Field('secret', env='SECRET_KEY')
    HOST: str = Field('localhost', env='HOST')
    PORT: int = Field(80, env='PORT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


# Load the configuration.
config = AppConfig()
app.config['SECRET_KEY'] = config.SECRET_KEY.get_secret_value()

# Set up the database connection and create the tables.
setup_db_connection(app)
create_tables()

# Set up the "uploads" folder.
setup_app_uploads(app)

# Import the views module, so that the routes are registered.
# noinspection PyUnresolvedReferences
import views
