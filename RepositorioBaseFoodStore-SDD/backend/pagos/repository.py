"""
Repositorio de Pagos — acceso a datos de la tabla `pagos`.

Sigue el mismo patrón que OrderRepository: opera sobre una sesión
inyectada por la Unidad de Trabajo para garantizar atomicidad.
"""

from typing import Optional
from sqlmodel import Session, select
from .models import Pago


class PagoRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, pago: Pago) -> Pago:
        self.session.add(pago)
        self.session.flush()  # obtener id sin commit
        self.session.refresh(pago)
        return pago

    def get_by_payment_id(self, payment_id: str) -> Optional[Pago]:
        """Usado para verificar idempotencia: si ya procesamos este payment_id."""
        statement = select(Pago).where(Pago.payment_id == payment_id)
        return self.session.exec(statement).one_or_none()

    def get_by_pedido_id(self, pedido_id: int) -> Optional[Pago]:
        """Último pago registrado para un pedido."""
        statement = (
            select(Pago)
            .where(Pago.pedido_id == pedido_id)
            .order_by(Pago.created_at.desc())
        )
        return self.session.exec(statement).first()

    def update_status(self, pago: Pago, mp_status: str, payment_id: Optional[str] = None, mp_status_detail: Optional[str] = None) -> Pago:
        pago.mp_status = mp_status
        if payment_id:
            pago.payment_id = payment_id
        if mp_status_detail:
            pago.mp_status_detail = mp_status_detail
        from datetime import datetime
        pago.updated_at = datetime.utcnow()
        self.session.add(pago)
        self.session.flush()
        self.session.refresh(pago)
        return pago
