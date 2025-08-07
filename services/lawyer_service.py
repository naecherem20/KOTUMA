from models.lawyer_models import Lawyer
from schema.lawyer_schemas import LawyerCreate
from sqlmodel import Session
from passlib.context import CryptContext
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_lawyer(lawyer_data: LawyerCreate, db: Session):
    if lawyer_data.password != lawyer_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = pwd_context.hash(lawyer_data.password)

    new_lawyer = Lawyer(
        full_name=lawyer_data.full_name,
        email=lawyer_data.email,
        phone_number=lawyer_data.phone_number,
        location=lawyer_data.location,
        year_of_experience=lawyer_data.year_of_experience,
        hashed_password=hashed_password
    )

    db.add(new_lawyer)
    db.commit()
    db.refresh(new_lawyer)

    return new_lawyer
