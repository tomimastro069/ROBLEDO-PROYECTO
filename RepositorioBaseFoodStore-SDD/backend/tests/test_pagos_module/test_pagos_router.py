import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.core.uow.unit_of_work import AppUnitOfWork
from pagos.router import crear_pago
from pagos.schemas import PagoCreate
from auth.schemas import TokenData
from orders.models import OrderStatus
import os
import uuid

def make_order_for_router(status_val="PENDIENTE"):
    from orders.models import Order, OrderStatus
    from decimal import Decimal
    from datetime import datetime
    order = Order(
        id=1,
        user_id=42,
        status=OrderStatus(status_val),
        total=Decimal("1500.00"),
        direccion_calle="Calle Falsa",
        direccion_numero="123",
        direccion_ciudad="Buenos Aires",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    return order

class TestPagosRouter:
    @patch("pagos.router._get_sdk")
    def test_crear_pago_transferencia_no_invoca_mp(self, mock_get_sdk):
        """Task 3.1: Comprobar que transferencia no invoque SDK de MP."""
        mock_uow = MagicMock(spec=AppUnitOfWork)
        mock_uow.orders.get.return_value = make_order_for_router("PENDIENTE")
        mock_uow.pagos.get_by_pedido_id.return_value = None
        
        # Mock payment persistence
        mock_pago = MagicMock()
        mock_pago.idempotency_key = "idemp-key-123"
        mock_uow.pagos.create.return_value = mock_pago
        
        data = PagoCreate(pedido_id=1, forma_pago_codigo="TRANSFERENCIA")
        current_user = TokenData(sub="42")
        
        # Configurar para que el context manager del mock funcione
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.__exit__.return_value = None
        
        result = crear_pago(data=data, current_user=current_user, uow=mock_uow)
        
        assert mock_get_sdk.called is False
        assert result.status == "pending"
        assert result.preference_id == "PREF-TRANSFERENCIA-idemp-ke"
        assert "forma_pago=TRANSFERENCIA" in result.init_point
        assert result.pedido_id == 1

    @patch("pagos.router.os.getenv")
    @patch("pagos.router._get_sdk")
    def test_crear_pago_sandbox_bypasses_mp(self, mock_get_sdk, mock_getenv):
        """Task 3.2: Comprobar que Sandbox (MERCADOPAGO con token TEST-) simula preferencia."""
        mock_uow = MagicMock(spec=AppUnitOfWork)
        mock_uow.orders.get.return_value = make_order_for_router("PENDIENTE")
        mock_uow.pagos.get_by_pedido_id.return_value = None
        
        mock_pago = MagicMock()
        mock_pago.idempotency_key = "idemp-key-123"
        mock_uow.pagos.create.return_value = mock_pago
        
        # Configurar context manager
        mock_uow.__enter__.return_value = mock_uow
        mock_uow.__exit__.return_value = None
        
        def getenv_side_effect(key, default=None):
            if key == "MP_ACCESS_TOKEN":
                return "TEST-access-token"
            return default
        mock_getenv.side_effect = getenv_side_effect
        
        data = PagoCreate(pedido_id=1, forma_pago_codigo="MERCADOPAGO")
        current_user = TokenData(sub="42")
        
        result = crear_pago(data=data, current_user=current_user, uow=mock_uow)
        
        assert mock_get_sdk.called is False
        assert result.status == "pending"
        assert result.preference_id.startswith("sandbox-")
        assert "sandbox=true" in result.init_point
        assert result.pedido_id == 1
