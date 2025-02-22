"""
Database Configuration Module.

This module sets up the database connection using SQLAlchemy with asynchronous support.
It defines the connection settings, creates the database engine, and provides a session factory 
for handling database interactions.

Environment Variables:
    DB_HOST_URL (str): The hostname and port of the database (default: "127.0.0.1:5432").
    DB_NAME (str): The name of the database (default: "database_name").
    DB_USER (str): The database username (default: "database_user").
    DB_PASSWORD (str): The database password (default: "database_password").

Attributes:
    SQLALCHEMY_DATABASE_URL (str): The complete database connection URL.
    engine (AsyncEngine): The SQLAlchemy asynchronous engine for database connections.
    async_session_maker (async_sessionmaker): Factory for creating asynchronous database sessions.
    Base (DeclarativeMeta): Base class for defining ORM models.

Functions:
    get_db(): Asynchronous generator that provides a database session.
"""
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession)


# Database configuration from environment variables
DB_HOST_URL = os.environ.get("DB_HOST_URL", "127.0.0.1:5432")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "123456")

# Database connection URL
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST_URL}/{DB_NAME}"

# Creating the asynchronous engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Session factory for handling database interactions
async_session_maker = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession)

# Base class for ORM models
Base = declarative_base()


async def get_db():
    """Provides a new database session for each request.

    This function is an asynchronous generator that creates a session
    using the async session factory and ensures it is properly closed after use.

    Yields:
        AsyncSession: A database session instance.
    """
    async with async_session_maker() as session:
        yield session
