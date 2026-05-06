import os
from fastapi import APIRouter, Request, Response, status
import mercadopago
from app.core.config import settings

router = APIRouter()

sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN", "test_your_mp_access_token"))

@router.post("/webhooks/mercadopago", status_code=status.HTTP_200_OK)
async def mercadopago_webhook(request: Request):
    body = await request.json()
    topic = request.query_params.get("topic")
    data_id = request.query_params.get("id")
    # For now, just log it. Update your business logic as needed.
    print(f"Received MercadoPago Webhook: topic={topic}, id={data_id}, body={body}")
    return Response(status_code=status.HTTP_200_OK)
