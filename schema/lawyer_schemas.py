from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

class LawyerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: int
    location: str
    year_of_experience: int

class LawyerCreate(LawyerBase):
    password: str
    confirm_password: str

class LawyerRead(LawyerBase):
    id: uuid.UUID

    class Config:
        from_attributes = True  # Use this if you are using Pydantic v2 (for ORM compatibility)
