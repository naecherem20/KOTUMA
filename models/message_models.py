from sqlmodel import SQLModel, Field
import uuid
from datetime import datetime

class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    sender_id: uuid.UUID = Field(index=True)
    receiver_id: uuid.UUID = Field(index=True)
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    is_read: bool = Field(default=False)
