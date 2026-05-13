"""
Modelo Pago — persistencia de transacciones con MercadoPago.

Responsabilidades:
  - Registrar cada intento de pago vinculado a un pedido.
  - Garantizar idempotencia mediante unicidad de idempotency_key y payment_id.
  - Proveer trazabilidad del ciclo de vida del pago (pending → approved / rejected / cancelled).

Relación: Un Pedido puede tener N intentos de Pago (reintentos tras rechazo),
pero solo uno puede quedar en estado 'approved'.
"""

from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
import uuid


class Pago(SQLModel, table=True):
    __tablename__ = "pagos"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Vínculo con el pedido
    pedido_id: int = Field(foreign_key="orders.id", index=True, nullable=False)

    # Datos de la preferencia de MercadoPago
    preference_id: Optional[str] = Field(default=None, index=True)

    # payment_id asignado por MP tras procesar la transacción (llega vía webhook)
    payment_id: Optional[str] = Field(default=None, unique=True, index=True)

    # Clave de idempotencia generada por NOSOTROS antes de llamar a MP
    # Garantiza que reintentos de red no generen cobros duplicados
    idempotency_key: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        unique=True,
        index=True,
        nullable=False,
    )

    # Estado nativo reportado por MP: pending, approved, rejected, cancelled
    mp_status: str = Field(default="pending", index=True)

    # Detalle del estado para mostrar en UI (ej: cc_rejected_insufficient_amount)
    mp_status_detail: Optional[str] = Field(default=None)

    # Auditoría
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
