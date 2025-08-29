from pydantic import BaseModel
from datetime import datetime
import uuid

class MessageCreate(BaseModel):
    sender_id: uuid.UUID
    receiver_id: uuid.UUID
    content: str

class MessageRead(BaseModel):
    id: uuid.UUID
    sender_id: uuid.UUID
    receiver_id: uuid.UUID
    content: str
    timestamp: datetime
    is_read: bool

    class Config:
        from_attributes = True  # pydantic v2 equivalent of orm_mode=True
