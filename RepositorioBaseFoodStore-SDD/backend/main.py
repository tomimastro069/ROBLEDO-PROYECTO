import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
sys.path.append("C:/Users/tomim/OneDrive/Escritorio/Robledo-parcial/ROBLEDO-PROYECTO/RepositorioBaseFoodStore-SDD")
from sqlmodel import SQLModel, create_engine
from backend.models import User

limiter = Limiter(key_func=lambda: "default-key")
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_middleware(SlowAPIMiddleware)
engine = create_engine("sqlite:///database.db")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
@limiter.limit("5/minute")
def read_root(request):
    return {"message": "Backend up and running!"}
