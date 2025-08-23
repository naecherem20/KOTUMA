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


auth_router=APIRouter(prefix="/auth", tags=["Authentication"])

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    full_name: str | None = None  # user id



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def decode_token(token: str = Depends(oauth2_scheme),    session: Session = Depends(get_session)):
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise cred_exc
        return TokenData(sub=sub)
    except JWTError:
        raise cred_exc
        
@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.query(User).filter(User.full_name == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@auth_router.get("/me")
def get_me(token_data: TokenData = Depends(decode_token), session: Session = Depends(get_session)):
    user = session.query(User).filter(User.id == int(token_data.sub)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username}




