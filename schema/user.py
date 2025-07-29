from pydantic import BaseModel
from pydantic import  EmailStr


class User_create(BaseModel):
    username: str
    email: EmailStr
    password: str