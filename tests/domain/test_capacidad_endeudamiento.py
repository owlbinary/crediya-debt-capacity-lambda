import pytest
from app.domain.capacidad_endeudamiento import Prestamo, Solicitante, evaluar_prestamo, Decision

class TestPrestamo:
    def test_cuota_mensual_sin_interes(self):
        prestamo = Prestamo(monto=1200, tasa_interes_anual=0, plazo_meses=12, estado='Aprobado')
        assert prestamo.cuota_mensual() == pytest.approx(100.0)

    def test_cuota_mensual_con_interes(self):
        prestamo = Prestamo(monto=10000, tasa_interes_anual=0.12, plazo_meses=12, estado='Aprobado')
        cuota = prestamo.cuota_mensual()
        assert cuota > 0

class TestSolicitante:
    def test_capacidad_endeudamiento_maxima(self):
        s = Solicitante(ingresos_totales=10000, salario=8000)
        assert s.capacidad_endeudamiento_maxima() == 3500

    def test_deuda_mensual_actual_sin_prestamos(self):
        s = Solicitante(ingresos_totales=10000, salario=8000)
        assert s.deuda_mensual_actual() == pytest.approx(0.0)

    def test_deuda_mensual_actual_con_deuda_total(self):
        s = Solicitante(ingresos_totales=10000, salario=8000, deuda_total_mensual=500)
        assert s.deuda_mensual_actual() == 500

    def test_deuda_mensual_actual_con_prestamos(self):
        p1 = Prestamo(monto=1200, tasa_interes_anual=0, plazo_meses=12, estado='Aprobado')
        p2 = Prestamo(monto=600, tasa_interes_anual=0, plazo_meses=6, estado='Pendiente')
        s = Solicitante(ingresos_totales=10000, salario=8000, prestamos=[p1, p2])
        assert s.deuda_mensual_actual() == pytest.approx(p1.cuota_mensual())

    def test_capacidad_disponible(self):
        s = Solicitante(ingresos_totales=10000, salario=8000, deuda_total_mensual=1000)
        assert s.capacidad_disponible() == 2500

class TestEvaluarPrestamo:
    def test_aprobado(self):
        s = Solicitante(ingresos_totales=10000, salario=2000, deuda_total_mensual=0)
        p = Prestamo(monto=1000, tasa_interes_anual=0, plazo_meses=10, estado='Pendiente')
        assert evaluar_prestamo(s, p) == Decision.APROBADO

    def test_revision_manual(self):
        s = Solicitante(ingresos_totales=10000, salario=1000, deuda_total_mensual=0)
        p = Prestamo(monto=6000, tasa_interes_anual=0, plazo_meses=12, estado='Pendiente')
        assert evaluar_prestamo(s, p) == Decision.REVISION_MANUAL

    def test_rechazado(self):
        s = Solicitante(ingresos_totales=1000, salario=1000, deuda_total_mensual=300)
        p = Prestamo(monto=10000, tasa_interes_anual=0.1, plazo_meses=12, estado='Pendiente')
        assert evaluar_prestamo(s, p) == Decision.RECHAZADO
