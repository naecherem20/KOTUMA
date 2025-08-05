from fastapi import FastAPI, Depends
from sqlmodel import SQLModel
from sqlmodel import Session , select
from models.user_models import User
from database.connection import engine, get_session
from router.V1.user import user_router
from router.V1.lawyer import router as lawyer_router   

app=FastAPI()
app.include_router(user_router)
app.include_router(lawyer_router, prefix="/api/v1/lawyers", tags=["Lawyers"])

@app.on_event("startup")
def on_startup():
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)

def init_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()





