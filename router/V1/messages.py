from fastapi import APIRouter, Depends, status
from typing import List
from sqlmodel import Session
from database.connection import get_session
from schema.message_schemas import MessageCreate, MessageRead
from services.message_service import (
    create_message_service,
    get_conversation_service,
    mark_read_service,
)
import uuid

router = APIRouter(prefix="/api/v1/messages", tags=["Messages"])

@router.post("/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
def send_message(payload: MessageCreate, session: Session = Depends(get_session)):
    return create_message_service(payload, session)

@router.get("/{user1_id}/{user2_id}", response_model=List[MessageRead])
def fetch_conversation(user1_id: uuid.UUID, user2_id: uuid.UUID, session: Session = Depends(get_session)):
    return get_conversation_service(user1_id, user2_id, session)

@router.post("/read/{partner_id}", response_model=int)
def mark_as_read(partner_id: uuid.UUID, me_id: uuid.UUID, session: Session = Depends(get_session)):
    """
    Example call: POST /api/v1/messages/read/{partner_id}?me_id=<my_uuid>
    Returns: number of messages marked read.
    """
    return mark_read_service(partner_id, me_id, session)
