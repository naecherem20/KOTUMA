from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import Session , select
from models.user_models import User
from database.connection import  get_session
from schema.user import User_create, User_show
from passlib.context import CryptContext
from auth import user_auth
from typing import Annotated



user_router=APIRouter(prefix="/v1/users")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@user_router.post("/signup", response_model=User_show, status_code=status.HTTP_201_CREATED)
def sign_up(user: User_create, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        phone=user.phone,
        city=user.city,
        state=user.state,
        situation_description=user.situation_description

    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@user_router.get("/all")
def all_users(session: Session = Depends(get_session)):
    users=session.exec(select(User)).all()
    return {"users":users}



