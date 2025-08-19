from fastapi import FastAPI
from sqlmodel import SQLModel
from database.connection import engine
from router.V1.user import user_router
from router.V1.lawyer import router as lawyer_router
from router.V1.lawyer_auth import router as lawyer_auth

app = FastAPI()
app.include_router(user_router)
app.include_router(lawyer_router)
app.include_router(lawyer_auth)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
