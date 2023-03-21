from pydantic import BaseSettings, Field, SecretStr


class DatabaseCredentials(BaseSettings):
    """Credentials for connecting to the database."""

    db_name: str = Field("catroom", env="DB_NAME")
    db_host: str = Field("localhost", env="DB_HOST")
    db_port: int = Field(5432, env="DB_PORT")
    db_username: str = Field("postgres", env="DB_USERNAME")
    db_password: SecretStr = Field("postgres", env="DB_PASSWORD")

    class Config:
        env_prefix = ""
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'
