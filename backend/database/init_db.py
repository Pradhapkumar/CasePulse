"""
Initialize Database
Run this script to create all database tables based on SQLAlchemy models.
"""
import sys
import os

# Add backend directory to sys.path to allow absolute imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db

if __name__ == "__main__":
    print("Initializing database tables...")
    init_db()
    print("Database tables created successfully.")
