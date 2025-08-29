from sqlmodel import Session, select
from models.message_models import Message
from schema.message_schemas import MessageCreate
from utils.webhook import send_webhook
import uuid
from typing import List

def create_message_service(message_data: MessageCreate, session: Session) -> Message:
    new_message = Message(
        sender_id=message_data.sender_id,
        receiver_id=message_data.receiver_id,
        content=message_data.content
    )
    session.add(new_message)
    session.commit()
    session.refresh(new_message)

    # fire-and-forget webhook (notify receiver, audit, etc.)
    send_webhook("message.received", new_message)

    return new_message

def get_conversation_service(user1_id: uuid.UUID, user2_id: uuid.UUID, session: Session) -> List[Message]:
    stmt = (
        select(Message)
        .where(
            ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
            ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
        )
        .order_by(Message.timestamp.asc())
    )
    return list(session.exec(stmt).all())

def mark_read_service(conversation_partner_id: uuid.UUID, me_id: uuid.UUID, session: Session) -> int:
    # optional helper to mark messages as read
    stmt = (
        select(Message)
        .where((Message.sender_id == conversation_partner_id) & (Message.receiver_id == me_id) & (Message.is_read == False))
    )
    items = list(session.exec(stmt).all())
    for m in items:
        m.is_read = True
        session.add(m)
    session.commit()
    return len(items)
