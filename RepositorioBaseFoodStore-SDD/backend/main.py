import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware

# Imports locales
from app.core.database import init_db
from app.core.seeder import run_seed
from auth.router import router as auth_router
from categories.router import router as categories_router
from products.router import router as products_router
from app.api.webhook_mercadopago import router as mp_webhook_router
from direcciones.router import router as direcciones_router
from perfil.router import router as perfil_router
from admin.router import router as admin_router
from pagos.router import router as pagos_router
from ingredientes.router import router as ingredientes_router
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
    
    # Ejecutar seeder automáticamente
    try:
        run_seed()
    except Exception as e:
        print(f"\n[SEEDER ERROR]: No se pudo completar el seeding: {e}\n")
    yield

app = FastAPI(
    title="FoodStore API",
    description="Backend para e-commerce de productos alimenticios",
    version="1.0.0",
    lifespan=lifespan
)

app.state.limiter = limiter

# Middlewares
import os as _os
_cors_origins = _os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)

# Register Orders service at /api/v1/orders
from orders import router as orders_router
app.include_router(orders_router, prefix="/api/v1/orders", tags=["orders"])

# Register Exception Handlers
app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include authentication routes
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
# Include categories routes
app.include_router(categories_router, prefix="/api/v1/categories", tags=["categories"])
# Include products routes
app.include_router(products_router, prefix="/api/v1/products", tags=["products"])
# Include direcciones routes
app.include_router(direcciones_router, prefix="/api/v1/direcciones", tags=["direcciones"])
# Include perfil routes
app.include_router(perfil_router, prefix="/api/v1/perfil", tags=["perfil"])
# Include admin routes
app.include_router(admin_router, prefix="/api/v1/admin", tags=["admin"])
# Include pagos routes
app.include_router(pagos_router, prefix="/api/v1/pagos", tags=["pagos"])
# Include ingredientes routes
app.include_router(ingredientes_router, prefix="/api/v1/ingredientes", tags=["ingredientes"])
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
