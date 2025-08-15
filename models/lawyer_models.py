from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr
import uuid

class LawyerBase(SQLModel):
    full_name: str
    email: EmailStr
    phone_number: int = Field(..., ge=1000000000, le=9999999999)  # Nigerian 10-digit number
    location: str
    year_of_experience: int = Field(..., ge=0)  # must be 0 or more

class LawyerCreate(LawyerBase):
    password: str
    confirm_password: str

class LawyerRead(LawyerBase):
    id: uuid.UUID

class Lawyer(LawyerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
