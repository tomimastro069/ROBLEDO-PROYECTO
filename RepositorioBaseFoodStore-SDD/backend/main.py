import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware

# Imports locales
from app.core.database import init_db
from auth.router import router as auth_router
from categories.router import router as categories_router
from products.router import router as products_router
from app.api.webhook_mercadopago import router as mp_webhook_router
from app.core.exceptions import DomainException, domain_exception_handler, validation_exception_handler

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

# Register Exception Handlers
app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
# Include categories routes
app.include_router(categories_router, prefix="/categories", tags=["categories"])
# Include products routes
app.include_router(products_router, prefix="/products", tags=["products"])
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
