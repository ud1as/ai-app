from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from configs.config import Settings  # Import your settings

# Load PostgreSQL credentials from settings
settings = Settings()

# SQLAlchemy database URL
DATABASE_URL = (
    f"postgresql+psycopg2://{settings.PGVECTOR_USER}:{settings.PGVECTOR_PASSWORD}"
    f"@{settings.PGVECTOR_HOST}:{settings.PGVECTOR_PORT}/{settings.PGVECTOR_DATABASE}"
)

# Index naming convention
POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
