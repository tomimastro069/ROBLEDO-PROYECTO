from fastapi import FastAPI
from app.core.config import settings
from app.core.database import init_db
from app.core.auth import router as auth_router

app = FastAPI()

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Backend up and running!"}
