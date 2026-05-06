import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware

# Imports locales
from app.core.database import init_db
from app.core.auth import router as auth_router
from app.api.webhook_mercadopago import router as mp_webhook_router
from models import User

# Configuration
limiter = Limiter(key_func=lambda: "default-key")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Mensaje de bienvenida premium
    print("\n" + "="*60)
    print("FOODSTORE BACKEND — Infrastructure")
    print("API Local: http://127.0.0.1:8000")
    print("Swagger UI: http://127.0.0.1:8000/docs")
    print("="*60 + "\n")
    
    # Inicializar base de datos
    init_db()
    yield

app = FastAPI(
    title="FoodStore API",
    description="Backend para e-commerce de productos alimenticios",
    version="1.0.0",
    lifespan=lifespan
)

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
# Include MercadoPago webhook router
app.include_router(mp_webhook_router, tags=["webhooks"])

@app.get("/")
@limiter.limit("5/minute")
def read_root(request: Request):
    return {
        "status": "online",
        "message": "FoodStore Backend up and running!",
        "version": "1.0.0"
    }
