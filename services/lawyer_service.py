from sqlmodel import Session
from fastapi import HTTPException
from models.lawyer_models import Lawyer
from schema.lawyer_schemas import LawyerCreate
import bcrypt

def register_lawyer_service(lawyer_data: LawyerCreate, session: Session):
    # Password match check
    if lawyer_data.password != lawyer_data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check if email already exists
    existing_lawyer = session.query(Lawyer).filter(Lawyer.email == lawyer_data.email).first()
    if existing_lawyer:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_pw = bcrypt.hashpw(
        lawyer_data.password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # Create lawyer record
    new_lawyer = Lawyer(
        full_name=lawyer_data.full_name,
        email=lawyer_data.email,
        phone_number=lawyer_data.phone_number,
        location=lawyer_data.location,
        year_of_experience=lawyer_data.year_of_experience,
        hashed_password=hashed_pw
    )
    session.add(new_lawyer)
    session.commit()
    session.refresh(new_lawyer)
    return new_lawyer
