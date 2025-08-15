from fastapi import FastAPI
from sqlmodel import SQLModel
from database.connection import engine
from router.V1.user import user_router
from router.V1.lawyer import router as lawyer_router

app = FastAPI()

# Register routers
app.include_router(user_router)
app.include_router(lawyer_router)

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Optional: This block only runs if you run main.py directly
if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)



