from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import Session , select
from models.user_models import User
from database.connection import  get_session

from schema.user import User_create, User_read
from passlib.context import CryptContext

user_router=APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@user_router.post("/", response_model=User_create, status_code=status.HTTP_201_CREATED)
def sign_up(user: User_create, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@user_router.get("/")
def all_users(session: Session = Depends(get_session)):
    users=session.exec(select(User)).all()
    return {"users":users}
