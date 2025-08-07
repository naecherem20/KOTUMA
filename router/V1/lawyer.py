from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database.connection import get_session
from schema.lawyer_schemas import LawyerCreate, LawyerRead
from services.lawyer_service import create_lawyer

router = APIRouter(prefix="/api/v1/lawyers", tags=["Lawyers"])

@router.post("/", response_model=LawyerRead, status_code=status.HTTP_201_CREATED)
def register_lawyer(lawyer_data: LawyerCreate, db: Session = Depends(get_session)):
    return create_lawyer(lawyer_data, db)
