from fastapi.testclient import TestClient
from app.adapters.api import app

client = TestClient(app)

def test_calcular_capacidad_success(monkeypatch):
    from app import adapters
    class DummyService:
        def calcular_y_actualizar_estado(self, solicitud_id, datos_solicitante, datos_prestamo, authorization=None):
            return {"solicitud_id": solicitud_id, "decision": "APROBADO"}
    monkeypatch.setattr(adapters.api, "service", DummyService())
    payload = {
        "solicitudId": "sol1",
        "salarioBase": 10000,
        "tipoPrestamo": {"tasaInteres": 0.1},
        "plazo": 12,
        "monto": 1000,
        "documentoIdentidad": "123",
        "deudaTotalMensual": 0,
        "token": "dummy-token"
    }
    response = client.post("/api/v1/calcular-capacidad", json=payload)
    assert response.status_code in (200, 201, 202)
    assert "decision" in response.json() or "error" in response.json()

def test_calcular_capacidad_incomplete():
    payload = {"solicitudId": "sol1", "token": "dummy-token"}
    response = client.post("/api/v1/calcular-capacidad", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data.get("codigo") == "VALIDATION_ERROR"
    assert "detalles" in data

