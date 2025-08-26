
from pydantic import BaseModel


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    full_name: str | None = None  # user id
    role: str | None = None


