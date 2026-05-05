"""
Database configuration and models
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - using SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency for getting database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    """
    Base.metadata.create_all(bind=engine)


# TODO: Define SQLAlchemy ORM models here
# Example:
# class CaseModel(Base):
#     __tablename__ = "cases"
#     id = Column(String, primary_key=True)
#     case_number = Column(String)
#     title = Column(String)
#     created_at = Column(DateTime, default=datetime.now)
