"""
Router de Pagos — endpoints para iniciar y consultar pagos con MercadoPago.

Responsabilidades:
  - POST /api/v1/pagos/crear: genera preferencia de pago con precio real del pedido
    e inyecta idempotency_key para prevenir cobros duplicados.
  - GET /api/v1/pagos/pedido/{pedido_id}: consulta el estado del pago de un pedido.

La clave de idempotencia (UUID) se persiste en la tabla `pagos` ANTES de
llamar a MercadoPago, garantizando que un reintento de red no genere
un segundo cobro.
"""

import os
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
import mercadopago

from pagos.schemas import PagoCreate, PagoRead
from pagos.models import Pago
from auth.dependencies import get_current_user
from auth.schemas import TokenData
from app.core.uow.unit_of_work import AppUnitOfWork, get_uow
from orders.models import OrderStatus

router = APIRouter()

_sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN", "TEST-your-mp-access-token"))


def _get_sdk():
    """Lazy accessor para facilitar el mock en tests."""
    return _sdk


@router.post("/crear", response_model=PagoRead, status_code=status.HTTP_201_CREATED)
def crear_pago(
    data: PagoCreate,
    current_user: TokenData = Depends(get_current_user),
    uow: AppUnitOfWork = Depends(get_uow),
):
    """
    Crea una preferencia de pago en MercadoPago para el pedido indicado.

    - Calcula el total REAL desde las líneas del pedido (precio inmutable snapshot).
    - Persiste la idempotency_key antes de llamar a MP.
    - Retorna el init_point (URL de checkout) y el preference_id.
    """
    with uow:
        # 1. Obtener pedido y verificar propiedad
        order = uow.orders.get(data.pedido_id)
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")
        if order.user_id != int(current_user.sub):
            raise HTTPException(status_code=403, detail="No autorizado para pagar este pedido.")
        if order.status != OrderStatus.PENDIENTE:
            raise HTTPException(
                status_code=409,
                detail=f"El pedido está en estado '{order.status.value}', no se puede iniciar pago."
            )

        # 2. Verificar si ya existe un pago aprobado para este pedido
        pago_existente = uow.pagos.get_by_pedido_id(data.pedido_id)
        if pago_existente and pago_existente.mp_status == "approved":
            raise HTTPException(status_code=409, detail="Este pedido ya fue pagado exitosamente.")

        # 3. Calcular total real desde snapshots inmutables del pedido
        total = float(order.total)

        # 4. Persistir el registro de pago con idempotency_key ANTES de llamar a MP
        nuevo_pago = Pago(
            pedido_id=data.pedido_id,
            idempotency_key=str(uuid.uuid4()),
            mp_status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        nuevo_pago = uow.pagos.create(nuevo_pago)

        # 5. Crear preferencia en MercadoPago usando el precio real
        preference_data = {
            "items": [
                {
                    "title": f"Pedido #{order.id} — Food Store",
                    "quantity": 1,
                    "unit_price": total,
                    "currency_id": "ARS",
                }
            ],
            "external_reference": str(order.id),
            "metadata": {
                "pedido_id": order.id,
                "user_id": current_user.sub,
                "idempotency_key": nuevo_pago.idempotency_key,
            },
            "back_urls": {
                "success": os.getenv("MP_SUCCESS_URL", "http://localhost:5173/pago/exito"),
                "failure": os.getenv("MP_FAILURE_URL", "http://localhost:5173/pago/error"),
                "pending": os.getenv("MP_PENDING_URL", "http://localhost:5173/pago/pendiente"),
            },
            "auto_return": "approved",
        }

        try:
            sdk = _get_sdk()
            response = sdk.preference().create(preference_data, {"X-Idempotency-Key": nuevo_pago.idempotency_key})
            result = response.get("response", {})
            if not result.get("id"):
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="No se pudo crear la preferencia en MercadoPago.",
                )

            # 6. Actualizar el registro con el preference_id retornado por MP
            nuevo_pago.preference_id = result.get("id")
            nuevo_pago.updated_at = datetime.utcnow()
            uow.pagos.update_status(nuevo_pago, "pending")

            return PagoRead(
                pedido_id=order.id,
                preference_id=result.get("id"),
                init_point=result.get("init_point"),
                status="pending",
            )

        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Error al conectar con MercadoPago: {str(exc)}",
            )


@router.get("/pedido/{pedido_id}", response_model=PagoRead, status_code=status.HTTP_200_OK)
def consultar_pago(
    pedido_id: int,
    current_user: TokenData = Depends(get_current_user),
    uow: AppUnitOfWork = Depends(get_uow),
):
    """Consulta el estado del último pago registrado para un pedido."""
    with uow:
        order = uow.orders.get(pedido_id)
        if not order:
            raise HTTPException(status_code=404, detail="Pedido no encontrado.")
        if order.user_id != int(current_user.sub):
            raise HTTPException(status_code=403, detail="No autorizado.")

        pago = uow.pagos.get_by_pedido_id(pedido_id)
        if not pago:
            return PagoRead(pedido_id=pedido_id, preference_id=None, init_point=None, status="not_found")

        return PagoRead(
            pedido_id=pedido_id,
            preference_id=pago.preference_id,
            init_point=None,
            status=pago.mp_status,
        )
