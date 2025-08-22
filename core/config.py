# from pydantic_settings import BaseSettings,SettingsConfigDict

# class Settings(BaseSettings):
#     DATABASE_URL: str

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         extra="ignore"
#     )
# settings=Settings()
# print(settings.model_dump())
from pydantic import BaseModel
import os
from datetime import timedelta

class Settings(BaseModel):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 20  # 20 min
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

settings = Settings()