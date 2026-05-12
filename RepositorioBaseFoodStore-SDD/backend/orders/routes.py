from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlmodel import Session as SQLSession, select
from typing import List
from auth.schemas import TokenData
from auth.dependencies import get_current_user, require_role
from auth.roles import Role
from .schemas import OrderCreate, OrderUpdate, OrderResponse
from .service import OrderService
from app.core.database import get_session
import uuid

router = APIRouter()

# Utilidad: Generación de correlation ID
async def get_correlation_id(request: Request):
    header = request.headers.get('x-correlation-id')
    if header:
        return header
    return str(uuid.uuid4())

# GET /health
@router.get("/health")
def health_check(session: SQLSession = Depends(get_session)):
    # Check DB
    try:
        session.exec(select(1))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return {
        "service": "orders",
        "status": "online" if db_status == "healthy" else "degraded",
        "dependencies": {
            "database": db_status
        }
    }

# POST /orders (usuario crea un pedido)
@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    session: SQLSession = Depends(get_session),
    current_user: TokenData = Depends(get_current_user),
    correlation_id: str = Depends(get_correlation_id)
):
    order_service = OrderService(session, correlation_id=correlation_id)
    order = order_service.create_order(user_id=int(current_user.sub), items=[i.dict() for i in payload.items], total=payload.total)
    return OrderResponse.from_orm(order)

# GET /orders/{id} (usuario/administrador obtiene un pedido)
@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    session: SQLSession = Depends(get_session),
    current_user: TokenData = Depends(get_current_user),
    correlation_id: str = Depends(get_correlation_id)
):
    order_service = OrderService(session, correlation_id=correlation_id)
    order = order_service.get_order(order_id)
    # Solo dueños o admin pueden leer el pedido
    if (order.user_id != int(current_user.sub)) and (current_user.role != Role.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para ver este pedido.")
    return OrderResponse.from_orm(order)

# GET /orders (usuario ve sus pedidos / admin lista todos)
@router.get("/orders", response_model=List[OrderResponse])
def list_orders(
    skip: int = 0,
    limit: int = 20,
    session: SQLSession = Depends(get_session),
    current_user: TokenData = Depends(get_current_user),
    correlation_id: str = Depends(get_correlation_id)
):
    order_service = OrderService(session, correlation_id=correlation_id)
    user_id = None if current_user.role == Role.ADMIN else int(current_user.sub)
    orders = (order_service.repo.list_all(skip, limit) if user_id is None else order_service.list_orders(user_id, skip, limit))
    return [OrderResponse.from_orm(order) for order in orders]

# PATCH /orders/{id} (actualizar estado pedido)
@router.patch("/orders/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    payload: OrderUpdate,
    session: SQLSession = Depends(get_session),
    current_user: TokenData = Depends(get_current_user),
    correlation_id: str = Depends(get_correlation_id)
):
    order_service = OrderService(session, correlation_id=correlation_id)
    order = order_service.get_order(order_id)
    # Sólo el dueño o admin puede modificar
    if (order.user_id != int(current_user.sub)) and (current_user.role != Role.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para editar este pedido.")
    updated_order = order_service.update_order(order_id, payload.dict(exclude_unset=True))
    return OrderResponse.from_orm(updated_order)

# DELETE /orders/{id} (cancelar pedido)
@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(
    order_id: int,
    session: SQLSession = Depends(get_session),
    current_user: TokenData = Depends(get_current_user),
    correlation_id: str = Depends(get_correlation_id)
):
    order_service = OrderService(session, correlation_id=correlation_id)
    order = order_service.get_order(order_id)
    # Sólo el dueño o admin puede cancelar
    if (order.user_id != int(current_user.sub)) and (current_user.role != Role.ADMIN):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para cancelar este pedido.")
    order_service.cancel_order(order_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
