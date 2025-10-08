from fastapi import FastAPI
from sqlmodel import SQLModel
from database.connection import engine
from router.V1.user import user_router
from router.V1.lawyer import router as lawyer_router
from auth.user_auth import auth_router
from auth.google_calender_auth import router as google_calender_router 
from router.V1.lawyer_auth import router as lawyer_auth_router
from fastapi.middleware.cors import CORSMiddleware
from router.V1.messages import router as messages_router

app = FastAPI()
app.include_router(user_router)
app.include_router(lawyer_router)
app.include_router(auth_router)
app.include_router(lawyer_auth_router)
app.include_router(messages_router)
app.include_router(google_calender_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["https://your-frontend.netlify.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
