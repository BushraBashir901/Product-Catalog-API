from sqlalchemy.orm import Session
from app.schemas.user import User,UserCreate,UserUpdate
from app.models.user import User
from app.core.security import hash_password


# Create new user
def create_user(db: Session, user: UserCreate, hashed_password: str):
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Get user by email (for login)
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


#Return all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


#Return single user
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

    
    

