import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

payment_completed_webhook = {
    "action": "payment.created",
    "data": {
        "id": "1234567890"  
    }
}

payment_failed_webhook = {
    "action": "payment.failed",
    "data": {
        "id": "0987654321"
    }
}

def test_webhook_payment_completed(monkeypatch):
    calls = {"log": None}
    
    def mock_print(*args, **kwargs):
        calls["log"] = args
    
    monkeypatch.setattr("builtins.print", mock_print)
    
    response = client.post("/webhooks/mercadopago?topic=payment&id=1234567890", json=payment_completed_webhook)
    assert response.status_code == 200
    # Check print output, means the handler logic ran
    assert calls["log"] is not None
    log_msg = calls["log"][0]
    assert "topic=payment" in log_msg
    assert "id=1234567890" in log_msg
    assert "payment.created" in str(log_msg)

def test_webhook_payment_failed(monkeypatch):
    calls = {"log": None}
    
    def mock_print(*args, **kwargs):
        calls["log"] = args
    
    monkeypatch.setattr("builtins.print", mock_print)
    
    response = client.post("/webhooks/mercadopago?topic=payment&id=0987654321", json=payment_failed_webhook)
    assert response.status_code == 200
    assert calls["log"] is not None
    log_msg = calls["log"][0]
    assert "topic=payment" in log_msg
    assert "id=0987654321" in log_msg
    assert "payment.failed" in str(log_msg)
