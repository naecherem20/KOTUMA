from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database.connection import get_session
from schema.lawyer_schemas import LawyerCreate, LawyerRead
from services.lawyer_service import register_lawyer_service

router = APIRouter(prefix="/api/v1/lawyers", tags=["Lawyers"])

@router.post("/", response_model=LawyerRead, status_code=status.HTTP_201_CREATED)
def register_lawyer(lawyer_data: LawyerCreate, session: Session = Depends(get_session)):
    return register_lawyer_service(lawyer_data, session)
