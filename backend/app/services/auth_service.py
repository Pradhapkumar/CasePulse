import hashlib
from sqlalchemy.orm import Session
from ..models import User
from ..schemas import SignupRequest

def hash_password(password: str) -> str:
    """Simple SHA256 hashing for hackathon prototype."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify if the provided password matches the stored hash."""
    return hash_password(password) == hashed_password

def create_demo_token(user: User) -> str:
    """Create a simple demo token for the user."""
    return f"casepulse-demo-token-{user.id}"

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, signup_data: SignupRequest):
    hashed_pwd = hash_password(signup_data.password)
    db_user = User(
        name=signup_data.name,
        email=signup_data.email,
        hashed_password=hashed_pwd,
        role=signup_data.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
