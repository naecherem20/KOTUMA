from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from models.lawyer_models import Lawyer, LawyerCreate, LawyerRead
from database.connection import get_session
from passlib.hash import bcrypt
from typing import List

router = APIRouter(prefix="/lawyers", tags=["Lawyers"])

@router.post("/", response_model=LawyerRead)
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

