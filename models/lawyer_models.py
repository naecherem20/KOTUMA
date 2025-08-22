from sqlmodel import SQLModel, Field,Relationship
import uuid
from typing import Optional,List,TYPE_CHECKING
from datetime import date,time, datetime
# from models.user_models import User


if TYPE_CHECKING:
    from models.user_models import User   # only for type hints


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

    appointments: List["Lawyer_appointment"] = Relationship(back_populates="lawyer")



class Lawyer_appointment(SQLModel,table=True):
    id: uuid.UUID= Field(default_factory=uuid.uuid4, primary_key=True)
    lawyer_id: uuid.UUID = Field(foreign_key="lawyer.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    booking_date:date
    booking_time:time
    status: str = Field(default="pending")

    lawyer: Optional["Lawyer"] = Relationship(back_populates="appointments")
    user: Optional["User"] = Relationship(back_populates="appointments")
