from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.security import verify_password,create_access_token,hash_password
from app.schemas.user import User,LoginRequest,LoginResponse,UserSignup,UserCreate
from app.crud import user as crud_user
from app.api.deps import get_db  #db for protected routes
from fastapi_cache.decorator import cache #chache concept


router=APIRouter(prefix="/auth",tags=["Auth"])

    
#login routes
@router.post("/login", response_model=LoginResponse,summary="Login User", description="User already register than login otherwise go to signup ")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    
    '''
    Authenticate a user by using email and password.
    
    steps:
    1.Check if user exist in database.
    2.verify the provided password
    3.Generate a jwt access token if credentials are valid.
    Raises:
         HTTPException 404: if email or password is incorrect.
    Returns:
          LoginResponse:Contain JWT access token  and bearer
    
    '''
    
    user = crud_user.get_user_by_email(db, login_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


#Signup routes
@router.post("/signup", response_model=User,summary="Signup", description="New users register here ")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    '''
    Register a new user in system.
    
    steps:
    1.Receive user data (name,email,password )
    2.Hashes the plain text hashed password
    3.store  new created user in database
    
    '''
    hashed = hash_password(user.password)
    return crud_user.create_user(db,UserCreate(name=user.name,email=user.email,password=user.password),hashed)
    


#Return all users in list 
@router.get("/", response_model=List[User],summary="Returns list of users ", description="Returns list of users that are registered ")
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''
    Retrieve users with pagination support.

    skip: Number of users to skip
    limit: Maximum number of users to return

    Returns a list of user objects.
    '''
    return crud_user.get_users(db, skip=skip, limit=limit)








