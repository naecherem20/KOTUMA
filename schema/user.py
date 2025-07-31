from pydantic import BaseModel
from pydantic import  EmailStr


class User_create(BaseModel):
    username: str
    email: EmailStr
    password: str

class User_read(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:    
        orm_mode = True
        