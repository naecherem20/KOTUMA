from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from models.lawyer_models import Lawyer
from database.connection import get_session
from core.security import verify_password, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/lawyer/login")
def login_lawyer(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    lawyer = session
