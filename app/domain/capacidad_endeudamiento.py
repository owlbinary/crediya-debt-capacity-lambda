
from dataclasses import dataclass
from typing import List, Optional
import math

class Decision:
	APROBADO = "APROBADO"
	RECHAZADO = "RECHAZADO"
	REVISION_MANUAL = "REVISION_MANUAL"

@dataclass
class Prestamo:
	monto: float
	tasa_interes_anual: float
	plazo_meses: int
	estado: str

	def cuota_mensual(self) -> float:
		"""Calcula la cuota mensual usando la fórmula de amortización."""
		if self.tasa_interes_anual == 0:
			return self.monto / self.plazo_meses
		i = self.tasa_interes_anual / 12
		n = self.plazo_meses
		P = self.monto
		cuota = (P * i * math.pow(1 + i, n)) / (math.pow(1 + i, n) - 1)
		return cuota


@dataclass
class Solicitante:
	ingresos_totales: float
	salario: float
	prestamos: Optional[List[Prestamo]] = None
	deuda_total_mensual: Optional[float] = None

	def capacidad_endeudamiento_maxima(self) -> float:
		return self.ingresos_totales * 0.35

	def deuda_mensual_actual(self) -> float:
		if self.deuda_total_mensual is not None:
			return self.deuda_total_mensual
		if self.prestamos:
			return sum(p.cuota_mensual() for p in self.prestamos if p.estado == 'Aprobado')
		return 0.0

	def capacidad_disponible(self) -> float:
		return self.capacidad_endeudamiento_maxima() - self.deuda_mensual_actual()

def evaluar_prestamo(solicitante: Solicitante, nuevo_prestamo: Prestamo) -> str:
	capacidad_disp = solicitante.capacidad_disponible()
	cuota_nuevo = nuevo_prestamo.cuota_mensual()
	if cuota_nuevo <= capacidad_disp:
		if nuevo_prestamo.monto > 5 * solicitante.salario:
			return Decision.REVISION_MANUAL
		return Decision.APROBADO
	else:
		return Decision.RECHAZADO
