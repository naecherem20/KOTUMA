from sqlmodel import Field
from pydantic import BaseModel, constr
import uuid
from datetime import date,time, datetime
from typing import Optional



class Lawyer_calender(BaseModel):
    lawyer_id: uuid.UUID 
    user_id: uuid.UUID 
    booking_date:date
    booking_time:time

class Consultation_info(BaseModel):
    full_name:str
    phone_number: constr(min_length=11, max_length=11,pattern=r"^\+234\d{10}$")
    purpose:str
    case_detail: Optional[str]=None
    upload_document:str