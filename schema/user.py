from sqlmodel import Field
from pydantic import BaseModel
from pydantic import  EmailStr
from pydantic import constr
from typing import Optional


class User_show(BaseModel):
    full_name: str
    email: EmailStr

class User_create(User_show):
    phone: constr(pattern=r'^\+234\s\d{3}\s\d{3}\s\d{4}$',max_length=17)
    city: str
    state:str
    situation_description:Optional[str]=Field(default=None)
    password: str
    confirm_password:str

class User_read(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:    
        orm_mode = True

