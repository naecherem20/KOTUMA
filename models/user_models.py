from sqlmodel import SQLModel, Field,Relationship
import uuid
from typing import Optional,List,TYPE_CHECKING
from pydantic import  EmailStr, constr
from models.lawyer_models import Lawyer_appointment


if TYPE_CHECKING:
    from models.lawyer_models import Lawyer_appointment


class User(SQLModel, table=True):
    id: uuid.UUID= Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str =Field(index=True)
    email: EmailStr
    phone: str= Field( nullable=False, max_length=17) 
    password: str  # hashed password
    city: str
    state:str
    situation_description:Optional[str]=Field(default=None)

    appointments: List["Lawyer_appointment"] = Relationship(back_populates="user")
