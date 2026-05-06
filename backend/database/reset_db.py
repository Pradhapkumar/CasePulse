"""
Reset Database
DANGER: This script will drop all tables and re-create them.
All existing data will be lost.
"""
import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base

def reset():
    print("WARNING: This will drop all tables and delete all data.")
    confirm = input("Are you sure you want to proceed? (yes/no): ")
    
    if confirm.lower() == 'yes':
        print("Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("Re-creating all tables...")
        Base.metadata.create_all(bind=engine)
        print("Database reset successfully.")
    else:
        print("Database reset cancelled.")

if __name__ == "__main__":
    reset()
