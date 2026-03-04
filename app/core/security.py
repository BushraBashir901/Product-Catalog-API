from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt,JWTError
from app.config import settings

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto") 

#Converting plain password into hashed password
def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72] # encode to bytes and truncate to 72 bytes
    return pwd_context.hash(password_bytes)


#Verifying hashed and plain password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")[:72]
    return pwd_context.verify(password_bytes, hashed_password)


# Create JWT token
def create_access_token(data: dict, expires_minutes: int = 30):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


#Decoding of Token
def decoded_access_token(token:str)->str:
    try:
        payload=jwt.decode(token, settings.SECRET_KEY,algorithms=["HS256"])
        return payload
    except JWTError:
        return None
        
        