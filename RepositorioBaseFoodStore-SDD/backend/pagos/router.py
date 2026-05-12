import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
import mercadopago

from pagos.schemas import PagoCreate, PagoRead
from auth.dependencies import get_current_user
from auth.schemas import TokenData

router = APIRouter()

_sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN", "test_your_mp_access_token"))


@router.post("/crear", response_model=PagoRead, status_code=status.HTTP_201_CREATED)
def crear_pago(
    data: PagoCreate,
    current_user: TokenData = Depends(get_current_user),
):
    """
    Crea una preferencia de pago en MercadoPago para el pedido indicado.
    Retorna el init_point (URL de checkout) y el preference_id.
    """
    idempotency_key = str(uuid.uuid4())

    preference_data = {
        "items": [
            {
                "title": f"Pedido #{data.pedido_id}",
                "quantity": 1,
                "unit_price": 1.0,  # el precio real se toma del pedido en producción
            }
        ],
        "external_reference": str(data.pedido_id),
        "metadata": {
            "pedido_id": data.pedido_id,
            "user_id": current_user.sub,
        },
        "back_urls": {
            "success": os.getenv("MP_SUCCESS_URL", "http://localhost:5173/pago/exito"),
            "failure": os.getenv("MP_FAILURE_URL", "http://localhost:5173/pago/error"),
            "pending": os.getenv("MP_PENDING_URL", "http://localhost:5173/pago/pendiente"),
        },
        "auto_return": "approved",
    }

    try:
        response = _sdk.preference().create(preference_data)
        result = response.get("response", {})
        if not result.get("id"):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="No se pudo crear la preferencia en MercadoPago.",
            )
        return PagoRead(
            pedido_id=data.pedido_id,
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
):
    """
    Consulta el estado de pago de un pedido usando su external_reference en MercadoPago.
    """
    try:
        response = _sdk.payment().search({"external_reference": str(pedido_id)})
        results = response.get("response", {}).get("results", [])
        if not results:
            return PagoRead(pedido_id=pedido_id, preference_id=None, init_point=None, status="not_found")
        last = results[-1]
        return PagoRead(
            pedido_id=pedido_id,
            preference_id=last.get("id"),
            init_point=None,
            status=last.get("status", "unknown"),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al consultar MercadoPago: {str(exc)}",
        )
