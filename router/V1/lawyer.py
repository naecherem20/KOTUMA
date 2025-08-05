from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from sqlalchemy import func
from models.lawyer_models import Lawyer, LawyerCreate, LawyerRead,LawyerBase
from database.connection import get_session
from passlib.hash import bcrypt
from typing import List

router = APIRouter(prefix="/lawyers", tags=["Lawyers"])

@router.post("/", response_model=LawyerRead,status_code=status.HTTP_201_CREATED)
def register_lawyer(lawyer_data: LawyerCreate, session: Session = Depends(get_session)):
    if lawyer_data.password != lawyer_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    existing_lawyer = session.exec(select(Lawyer).where(Lawyer.email == lawyer_data.email)).first()
    if existing_lawyer:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = bcrypt.hash(lawyer_data.password)
    new_lawyer = Lawyer(
        full_name=lawyer_data.full_name,
        email=lawyer_data.email,
        phone_number=lawyer_data.phone_number,
        hashed_password=hashed_pw
    )
    session.add(new_lawyer)
    session.commit()
    session.refresh(new_lawyer)
    return new_lawyer

@router.get("/{full_name}", response_model=LawyerBase)
def find_lawyers(full_name:str, session: Session = Depends(get_session)):
    existing_lawyer = session.exec(select(Lawyer).where(func.upper(Lawyer.full_name) == full_name.upper())).first()
    if not existing_lawyer:
        raise HTTPException(status_code=404, detail="Lawyer not found!!")
    return existing_lawyer

