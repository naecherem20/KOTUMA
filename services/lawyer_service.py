from fastapi import HTTPException
from sqlmodel import Session, select

from core.security import get_password_hash
from models.lawyer_models import Lawyer
from schema.lawyer_schemas import LawyerCreate

def register_lawyer_service(lawyer_data: LawyerCreate, session: Session) -> Lawyer:
    if lawyer_data.password != lawyer_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # check duplicate email
    exists = session.exec(select(Lawyer).where(Lawyer.email == lawyer_data.email)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_lawyer = Lawyer(
        full_name=lawyer_data.full_name,
        email=lawyer_data.email,
        phone_number=lawyer_data.phone_number,
        location=lawyer_data.location,
        year_of_experience=lawyer_data.year_of_experience,
        hashed_password=get_password_hash(lawyer_data.password),
    )
    session.add(new_lawyer)
    session.commit()
    session.refresh(new_lawyer)
    return new_lawyer
