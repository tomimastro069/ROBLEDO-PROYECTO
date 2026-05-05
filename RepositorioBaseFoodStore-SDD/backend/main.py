import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from sqlmodel import SQLModel, create_engine

# Path setup for local imports
sys.path.append("C:/Users/tomim/OneDrive/Escritorio/Robledo-parcial/ROBLEDO-PROYECTO/RepositorioBaseFoodStore-SDD")
from backend.models import User

# Configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
engine = create_engine(DATABASE_URL)
limiter = Limiter(key_func=lambda: "default-key")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Mensaje de bienvenida premium
    print("\n" + "="*60)
    print("FOODSTORE BACKEND — Sprint 0 Infrastructure")
    print("API Local: http://127.0.0.1:8000")
    print("Swagger UI: http://127.0.0.1:8000/docs")
    print("="*60 + "\n")
    
    # Crear tablas si no existen según los modelos de SQLModel
    SQLModel.metadata.create_all(engine)
    yield
    # Shutdown: Limpieza si fuera necesaria

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter

# Middlewares
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)
app.add_middleware(SlowAPIMiddleware)

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
@limiter.limit("5/minute")
def read_root(request: Request):
    return {"message": "Backend up and running!"}
