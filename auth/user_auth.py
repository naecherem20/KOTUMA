from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session , select
from typing import Annotated
from pydantic import BaseModel
from models.user_models import User
from jose import JWTError,jwt
from passlib.context import CryptContext
from database.connection import get_session
from core.config import settings
from datetime import datetime,timedelta
from schema.user_auth_schema import Token,TokenData
import uuid


auth_router=APIRouter(prefix="/api/v1/auth/user", tags=["Authentication"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme_user = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/user/login",scheme_name="UserAuth")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def decode_token(token: Annotated[str,  Depends(oauth2_scheme_user)],    session: Session = Depends(get_session)):
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        role = payload.get("role")
        if sub is None or role != "user": 
            raise cred_exc
        token_data = TokenData(sub=sub,role=role)
    except JWTError:
        raise cred_exc
    user_id = uuid.UUID(sub)
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise cred_exc
    return user

        
@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": str(user.id), "role": "user"})
    return {"access_token": token, "token_type": "bearer"}

@auth_router.get("/me")
def get_me(current_user: Annotated[User, Depends(decode_token)]):
    return {"id": current_user.id, "username": current_user.email,"message":"you've been logged in!!"}
    