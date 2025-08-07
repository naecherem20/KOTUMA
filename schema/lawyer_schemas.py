from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class LawyerBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: int = Field(..., ge=1000000000, le=9999999999)
    location: str
    year_of_experience: int

class LawyerCreate(LawyerBase):
    password: str
    confirm_password: str

class LawyerRead(LawyerBase):
    id: UUID
