from app.application.capacidad_service import CapacidadEndeudamientoService
from app.domain.capacidad_endeudamiento import Decision

class DummyRepository:
    def __init__(self):
        self.last_update = None

    def actualizar_estado_solicitud(self, solicitud_id, nuevo_estado, plan_pago=None, monto=None, tasa_interes=None, plazo=None):
        self.last_update = (solicitud_id, nuevo_estado, monto, tasa_interes, plazo)
        return True, None

class TestCapacidadEndeudamientoService:
    def test_calcular_y_actualizar_estado_aprobado(self):
        repo = DummyRepository()
        service = CapacidadEndeudamientoService(repo)
        datos_solicitante = {"ingresos_totales": 10000, "salario": 2000}
        datos_prestamo = {"monto": 1000, "tasa_interes_anual": 0, "plazo_meses": 10}
        result = service.calcular_y_actualizar_estado("sol1", datos_solicitante, datos_prestamo)
        assert result["decision"] == Decision.APROBADO
        assert repo.last_update == ("sol1", Decision.APROBADO)

    def test_calcular_y_actualizar_estado_revision_manual(self):
        repo = DummyRepository()
        service = CapacidadEndeudamientoService(repo)
        datos_solicitante = {"ingresos_totales": 10000, "salario": 1000}
        datos_prestamo = {"monto": 6000, "tasa_interes_anual": 0, "plazo_meses": 12}
        result = service.calcular_y_actualizar_estado("sol2", datos_solicitante, datos_prestamo)
        assert result["decision"] == Decision.REVISION_MANUAL
        assert repo.last_update == ("sol2", Decision.REVISION_MANUAL)

    def test_calcular_y_actualizar_estado_rechazado(self):
        repo = DummyRepository()
        service = CapacidadEndeudamientoService(repo)
        datos_solicitante = {"ingresos_totales": 1000, "salario": 1000, "deuda_total_mensual": 300}
        datos_prestamo = {"monto": 10000, "tasa_interes_anual": 0.1, "plazo_meses": 12}
        result = service.calcular_y_actualizar_estado("sol3", datos_solicitante, datos_prestamo)
        assert result["decision"] == Decision.RECHAZADO
        assert repo.last_update == ("sol3", Decision.RECHAZADO)

    def test_error_handling(self):
        repo = DummyRepository()
        service = CapacidadEndeudamientoService(repo)
        datos_solicitante = {"ingresos_totales": 1000, "salario": 1000}
        datos_prestamo = {"monto": None, "tasa_interes_anual": 0.1, "plazo_meses": 12}
        result = service.calcular_y_actualizar_estado("sol4", datos_solicitante, datos_prestamo)
        assert "error" in result
