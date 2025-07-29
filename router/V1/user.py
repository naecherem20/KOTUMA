from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import Session , select
from models.user_models import User
from database.connection import  get_session

from schema.user import User_create


user_router=APIRouter()
@user_router.post("/", response_model=User_create, status_code=status.HTTP_201_CREATED)
def sign_up(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@user_router.get("/")
def all_users(session: Session = Depends(get_session)):
    users=session.exec(select(User)).all()
    return {"users":users}
