from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os


# Load .env file
load_dotenv()

# Get DB URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing. Please check your .env file!")


# Create engine and session
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session