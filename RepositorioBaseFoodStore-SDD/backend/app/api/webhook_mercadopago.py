"""
Webhook IPN de MercadoPago — procesamiento asíncrono de notificaciones de pago.

Flujo:
  1. Recibir notificación POST de MercadoPago.
  2. Verificar idempotencia: si el payment_id ya fue procesado, responder 200 OK.
  3. Consultar detalles del pago a la API de MP.
  4. Si status == 'approved':
     a. Actualizar registro `Pago` en la DB.
     b. Confirmar el pedido vía OrderService.confirm_by_payment (FSM PENDIENTE→CONFIRMADO).
     Todo dentro de UoW (una sola transacción atómica).
  5. Si status == 'rejected' o 'cancelled': registrar pero NO avanzar el pedido.

Idempotencia estricta:
  - Si ya existe un Pago con ese payment_id en estado 'approved', devuelve 200 sin reejecutar.
  - Si el pedido ya está en CONFIRMADO o superior, devuelve 200 sin reejecutar.

Referencia: RN-03 (auditoría append-only), Design Decision #2 (límites UoW).
"""

import hashlib
import hmac
import logging
import os

from fastapi import APIRouter, Request, HTTPException, status, Depends
from datetime import datetime

from app.core.uow.unit_of_work import AppUnitOfWork, get_uow
from orders.service import OrderService
from orders.models import OrderStatus
from orders.exceptions import OrderNotFoundException, InvalidStateTransitionException

logger = logging.getLogger("webhook.mercadopago")

router = APIRouter()

MP_WEBHOOK_SECRET = os.getenv("MP_WEBHOOK_SECRET", "")


def _verify_signature(request_headers: dict, raw_body: bytes) -> bool:
    """
    Verifica la firma HMAC-SHA256 del webhook de MercadoPago.
    Retorna True si la firma es válida o si no hay secret configurado (dev mode).

    Documentación: https://www.mercadopago.com.ar/developers/es/docs/your-integrations/notifications/webhooks
    """
    if not MP_WEBHOOK_SECRET:
        logger.warning("MP_WEBHOOK_SECRET no configurado — omitiendo verificación de firma (dev mode).")
        return True

    x_signature = request_headers.get("x-signature", "")
    x_request_id = request_headers.get("x-request-id", "")

    # Extraer ts y v1 del header x-signature
    parts = dict(part.split("=", 1) for part in x_signature.split(",") if "=" in part)
    ts = parts.get("ts", "")
    v1 = parts.get("v1", "")

    if not ts or not v1:
        return False

    # Construir el manifest para verificar
    # Formato: id:[data.id_value];request-id:[x-request-id_value];ts:[ts_value];
    # Para notificaciones de tipo 'payment', data.id es el payment_id en el query param
    manifest = f"id:{request_headers.get('data_id', '')};request-id:{x_request_id};ts:{ts};"
    expected = hmac.new(MP_WEBHOOK_SECRET.encode(), manifest.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(expected, v1)


@router.post("/mercadopago", status_code=status.HTTP_200_OK)
async def mercadopago_webhook(
    request: Request,
    uow: AppUnitOfWork = Depends(get_uow),
):
    """
    Endpoint de recepción de notificaciones IPN de MercadoPago.

    MP siempre espera HTTP 200 OK. Cualquier otro código causará reintentos.
    La lógica de negocio es idempotente: reintentos son seguros.
    """
    body = await request.body()
    headers = dict(request.headers)

    # Extraer data.id del query param (MP lo envía como ?data.id=xxx&type=payment)
    data_id = request.query_params.get("data.id", "")
    headers["data_id"] = data_id
    topic = request.query_params.get("type", "")

    logger.info(f"Webhook recibido — type: {topic}, data.id: {data_id}")

    # Solo procesamos notificaciones de tipo 'payment'
    if topic != "payment" or not data_id:
        logger.info(f"Webhook ignorado — type={topic} data_id={data_id}")
        return {"status": "ignored"}

    # Verificar firma HMAC
    if not _verify_signature(headers, body):
        logger.warning(f"Webhook con firma inválida — data_id={data_id}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Firma inválida.")

    # Procesar dentro de una transacción atómica
    with uow:
        # ── Idempotencia: verificar si ya procesamos este payment_id ──
        pago_existente = uow.pagos.get_by_payment_id(data_id)
        if pago_existente and pago_existente.mp_status == "approved":
            logger.info(f"payment_id={data_id} ya procesado (approved). Respondiendo 200 idempotente.")
            return {"status": "already_processed"}

        # ── Consultar estado real del pago a la API de MP ──
        try:
            import mercadopago
            sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN", ""))
            payment_info = sdk.payment().get(data_id)
            payment_data = payment_info.get("response", {})
        except Exception as exc:
            logger.error(f"Error consultando payment {data_id} a MP: {exc}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Error consultando MercadoPago API."
            )

        mp_status = payment_data.get("status", "unknown")
        mp_status_detail = payment_data.get("status_detail", "")
        external_reference = payment_data.get("external_reference")  # = order.id

        logger.info(f"payment_id={data_id} status={mp_status} pedido_id={external_reference}")

        if not external_reference:
            logger.warning(f"Webhook sin external_reference para payment_id={data_id}")
            return {"status": "no_reference"}

        pedido_id = int(external_reference)

        # ── Verificar si el pedido ya está en estado superior (idempotencia de FSM) ──
        order = uow.orders.get(pedido_id)
        if not order:
            logger.error(f"Pedido {pedido_id} no encontrado para payment_id={data_id}")
            return {"status": "order_not_found"}

        if order.status != OrderStatus.PENDIENTE:
            logger.info(f"Pedido {pedido_id} ya en estado {order.status} — ignorando webhook.")
            return {"status": "order_already_advanced"}

        # ── Actualizar o crear registro de Pago ──
        if pago_existente:
            uow.pagos.update_status(
                pago_existente,
                mp_status=mp_status,
                payment_id=data_id,
                mp_status_detail=mp_status_detail,
            )
            pago = pago_existente
        else:
            from pagos.models import Pago
            import uuid
            pago = Pago(
                pedido_id=pedido_id,
                payment_id=data_id,
                idempotency_key=str(uuid.uuid4()),
                mp_status=mp_status,
                mp_status_detail=mp_status_detail,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            pago = uow.pagos.create(pago)

        # ── Avanzar FSM del pedido si el pago fue aprobado ──
        if mp_status == "approved":
            try:
                order_service = OrderService(uow)
                order_service.confirm_by_payment(pedido_id, uow)
                logger.info(f"Pedido {pedido_id} confirmado exitosamente vía webhook.")
            except (OrderNotFoundException, InvalidStateTransitionException) as exc:
                logger.error(f"Error confirmando pedido {pedido_id}: {exc}")
                # No re-lanzar — MP no debe reintentar por errores de FSM
                return {"status": "fsm_error", "detail": str(exc)}
        elif mp_status in ("rejected", "cancelled"):
            logger.info(f"Pago {data_id} {mp_status} — pedido {pedido_id} permanece PENDIENTE para reintento.")

    return {"status": "processed", "mp_status": mp_status}
