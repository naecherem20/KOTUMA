from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from sqlalchemy import func
from fastapi import APIRouter, Depends, status
from passlib.hash import bcrypt
from typing import List
from models.lawyer_models import Lawyer, LawyerCreate, LawyerRead,LawyerBase,Lawyer_appointment
from database.connection import get_session
from schema.lawyer import Lawyer_calender
from models.user_models import User
from schema.lawyer_schemas import LawyerCreate, LawyerRead
from services.lawyer_service import register_lawyer_service

router = APIRouter(prefix="/v1/lawyers", tags=["Lawyers"])

@router.post("/", response_model=LawyerRead, status_code=status.HTTP_201_CREATED)
def register_lawyer(lawyer_data: LawyerCreate, session: Session = Depends(get_session)):
    return register_lawyer_service(lawyer_data, session)

@router.get("/{full_name}", response_model=LawyerBase)
def find_lawyers(full_name:str, session: Session = Depends(get_session)):
    existing_lawyer = session.exec(select(Lawyer).where(func.upper(Lawyer.full_name) == full_name.upper())).first()
    if not existing_lawyer:
        raise HTTPException(status_code=404, detail="Lawyer not found!!")
    return existing_lawyer

@router.post("/appointment",  response_model=Lawyer_calender ,status_code=status.HTTP_201_CREATED)
def lawyer_calender(appointment:Lawyer_calender,session: Session = Depends(get_session),):
    lawyer = session.get(Lawyer,appointment.lawyer_id)
    user = session.get(User, appointment.user_id)
    if not lawyer:
        raise HTTPException(status_code=404, detail="Lawyer not found")
    if not user:
        raise HTTPException(status_code=404, detail="This user does not exist")
    booking = Lawyer_appointment(
        lawyer_id=lawyer.id,
        user_id=user.id,
        booking_date=appointment.booking_date,
        booking_time=appointment.booking_time,
        status="pending"
    )
    session.add(booking)
    session.commit()
    session.refresh(booking)

    return booking
