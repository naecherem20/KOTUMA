from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import  EmailStr


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str =Field(index=True)
    email: EmailStr
    phone: str = Field(max_length=11)
    password: str  # hashed password
    city: str
    state:str
    situation_description:Optional[str]=Field(default=None)
