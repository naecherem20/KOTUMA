from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from core.security import create_access_token, verify_password, get_current_lawyer
from database.connection import get_session
from models.lawyer_models import Lawyer
from schema.auth_schemas import Token
from schema.lawyer_schemas import LawyerRead

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/lawyer/login", response_model=Token)
def login_lawyer(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    # OAuth2 uses `username` for the identifier; we use email
    lawyer = session.exec(select(Lawyer).where(Lawyer.email == form_data.username)).first()
    if not lawyer or not verify_password(form_data.password, lawyer.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": str(lawyer.id)}, expires_delta=timedelta(minutes=60))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/lawyer/me", response_model=LawyerRead)
def read_current_lawyer(current_lawyer: Lawyer = Depends(get_current_lawyer)):
    return current_lawyer
