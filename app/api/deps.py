from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import settings

security=HTTPBearer()

#Dependency for routes
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),db: Session = Depends(get_db)):
    
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms='HS256'
        )
        email = payload.get("sub")

        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user