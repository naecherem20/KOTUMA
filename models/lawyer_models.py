from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

class LawyerBase(SQLModel):
    full_name: str
    email: str
    phone_number: str

class LawyerCreate(LawyerBase):
    password: str
    confirm_password: str

class LawyerRead(LawyerBase):
    id: uuid.UUID

class Lawyer(LawyerBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
