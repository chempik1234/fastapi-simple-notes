import os
from pydantic_settings import BaseSettings
# from dotenv import get_key

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ENV_PATH = os.path.join(BASE_DIR, '.env')


class Settings(BaseSettings):
    POSTGRES_DATABASE_URL: str = os.getenv("POSTGRES_DATABASE_URL")  # get_key(ENV_PATH, "POSTGRES_DATABASE_URL")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY") # get_key(ENV_PATH, "JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY") # get_key(ENV_PATH, "JWT_REFRESH_SECRET_KEY")
    # SQLALCHEMY_DATABASE_URL: str = get_key(ENV_PATH, "SQLALCHEMY_DATABASE_URL")
    # SYNC_SQLALCHEMY_DATABASE_URL: str = get_key(ENV_PATH, "SYNC_SQLALCHEMY_DATABASE_URL")
    # TEST_SQLALCHEMY_DATABASE_URL: str = get_key(ENV_PATH, "TEST_SQLALCHEMY_DATABASE_URL")
    # TEST_DB_NAME: str = get_key(ENV_PATH, "TEST_DB_NAME")


settings = Settings()
