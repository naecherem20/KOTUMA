from sqlmodel import SQLModel, Field
from pydantic import EmailStr
import uuid

class LawyerBase(SQLModel):
    full_name: str
    email: EmailStr
    phone_number: int = Field(..., ge=1000000000, le=9999999999)
    location: str
    year_of_experience: int = Field(..., ge=0)

class Lawyer(LawyerBase, table=True):
    __tablename__ = "lawyer"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

class LawyerCreate(LawyerBase):
    password: str
    confirm_password: str

class LawyerRead(LawyerBase):
    id: uuid.UUID
    # Pydantic v2: replaces orm_mode=True
    model_config = {"from_attributes": True}
