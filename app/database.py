from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings  # Ensure this import works

# Correct database credentials
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}/{settings.database_name}"
)

# Create SQLAlchemy engine and session factory
engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Provide a database session to routes."""
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
