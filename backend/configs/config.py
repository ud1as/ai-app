import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Configuration class for application settings.
    All settings are fetched directly from environment variables using os.getenv.
    """

    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "your_openai_api_key")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-mini")

    # Embedding Model Settings
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

    # MongoDB Settings
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

    # AWS Settings
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "your_aws_access_key_id")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "your_aws_secret_access_key")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    S3_BUCKET: str = os.getenv("S3_BUCKET", "your_s3_bucket_name")

    # PGVector Settings
    PGVECTOR_HOST: str = os.getenv("PGVECTOR_HOST", "localhost")
    PGVECTOR_PORT: int = int(os.getenv("PGVECTOR_PORT", 5432))
    PGVECTOR_USER: str = os.getenv("PGVECTOR_USER", "postgres")
    PGVECTOR_PASSWORD: str = os.getenv("PGVECTOR_PASSWORD", "password")
    PGVECTOR_DATABASE: str = os.getenv("PGVECTOR_DATABASE", "example_db")
    PGVECTOR_MIN_CONNECTION: int = int(os.getenv("PGVECTOR_MIN_CONNECTION", 1))
    PGVECTOR_MAX_CONNECTION: int = int(os.getenv("PGVECTOR_MAX_CONNECTION", 10))

    # Aliases for PG compatibility
    PG_USER: str = PGVECTOR_USER
    PG_PASSWORD: str = PGVECTOR_PASSWORD
    PG_HOST: str = PGVECTOR_HOST
    PG_PORT: int = PGVECTOR_PORT
    PG_DATABASE: str = PGVECTOR_DATABASE


# Instantiate the settings
config = Settings()
