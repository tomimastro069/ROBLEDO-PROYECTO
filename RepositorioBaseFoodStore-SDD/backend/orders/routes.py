from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session as SQLSession
from typing import List, Optional
from auth.schemas import TokenData
from auth.dependencies import get_current_user, require_role
from auth.roles import Role
from .schemas import OrderCreate, OrderRead, OrderAdminRead, StateChangeRequest
from .service import OrderService
from .exceptions import OrderNotFoundException, InvalidStateTransitionException
from app.core.database import get_session
import uuid

router = APIRouter()

# Dependency Factory for OrderService
def get_order_service(
    session: SQLSession = Depends(get_session),
    request: Request = None
):
    correlation_id = request.headers.get('x-correlation-id', str(uuid.uuid4()))
    return OrderService(session, correlation_id=correlation_id)

# Customer Endpoints
@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    service: OrderService = Depends(get_order_service),
    current_user: TokenData = Depends(get_current_user)
):
    # En un caso real, buscaríamos los precios actuales de los productos aquí
    # Para esta fase, los pasamos como dicts
    items_data = [item.dict() for item in payload.items]
    order = service.create_order(user_id=int(current_user.sub), items=items_data)
    return order

@router.get("/", response_model=List[OrderRead])
def list_my_orders(
    skip: int = 0,
    limit: int = 20,
    service: OrderService = Depends(get_order_service),
    current_user: TokenData = Depends(get_current_user)
):
    return service.list_orders(user_id=int(current_user.sub), skip=skip, limit=limit)

@router.get("/{order_id}", response_model=OrderRead)
def get_order_detail(
    order_id: int,
    service: OrderService = Depends(get_order_service),
    current_user: TokenData = Depends(get_current_user)
):
    order = service.get_order(order_id)
    if order.user_id != int(current_user.sub) and current_user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="No autorizado para ver este pedido.")
    return order

@router.patch("/{order_id}/cancel", response_model=OrderRead)
def cancel_order(
    order_id: int,
    payload: StateChangeRequest,
    service: OrderService = Depends(get_order_service),
    current_user: TokenData = Depends(get_current_user)
):
    order = service.get_order(order_id)
    
    # RBAC Dinámico (RN-RB08 / RN-FS08)
    if order.user_id != int(current_user.sub) and current_user.role not in [Role.ADMIN, Role.GESTOR_PEDIDOS]:
        raise HTTPException(status_code=403, detail="No autorizado para cancelar este pedido.")
    
    try:
        service.cancel_order(order_id, reason=payload.reason)
        return service.get_order(order_id)
    except InvalidStateTransitionException as e:
        raise HTTPException(status_code=400, detail=str(e))

# Admin/Gestor Endpoints
@router.get("/admin/orders", response_model=List[OrderAdminRead])
def list_all_orders(
    skip: int = 0,
    limit: int = 20,
    service: OrderService = Depends(get_order_service),
    admin: TokenData = Depends(require_role(Role.ADMIN, Role.GESTOR_PEDIDOS))
):
    return service.list_orders(user_id=None, skip=skip, limit=limit)

@router.patch("/admin/orders/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    payload: StateChangeRequest,
    service: OrderService = Depends(get_order_service),
    admin: TokenData = Depends(require_role(Role.ADMIN, Role.GESTOR_PEDIDOS))
):
    if not payload.new_status:
        raise HTTPException(status_code=400, detail="Debe especificar el nuevo estado.")
    
    try:
        return service.update_order(order_id, {"status": payload.new_status})
    except InvalidStateTransitionException as e:
        raise HTTPException(status_code=400, detail=str(e))
