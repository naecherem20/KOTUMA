from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import  EmailStr


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: EmailStr
    password: str  # hashed password
