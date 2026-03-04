from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

#REQUEST SCHEMAS
#All comman fields are in Base schema
class UserBase(BaseModel):
    name: str
    email: EmailStr  

class UserCreate(UserBase):
    password: str  

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    password: Optional[str]  
    
class UserSignup(BaseModel):
    name:str
    email:EmailStr
    password:str
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
    
#RESPONSE SCHEMA 
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }