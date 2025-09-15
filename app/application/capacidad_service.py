
from app.domain.capacidad_endeudamiento import Solicitante, Prestamo, evaluar_prestamo, Decision
from decimal import Decimal, getcontext, ROUND_HALF_UP
from app.infrastructure.logger import get_logger


logger = get_logger()

class CapacidadEndeudamientoService:
	def __init__(self, repository):
		self.repository = repository

	def calcular_y_actualizar_estado(self, solicitud_id: str, datos_solicitante: dict, datos_prestamo: dict) -> dict:
		"""
		Orquesta el cálculo de capacidad y actualiza el estado de la solicitud de forma atómica.
		Maneja logs y excepciones. Si el tipo de préstamo tiene validación automática, encola la solicitud.
		"""
		try:
			logger.info(f"Iniciando cálculo de capacidad para solicitud {solicitud_id}")
			solicitante = Solicitante(
				ingresos_totales=datos_solicitante['ingresos_totales'],
				salario=datos_solicitante['salario'],
				deuda_total_mensual=datos_solicitante.get('deuda_total_mensual')
			)
			nuevo_prestamo = Prestamo(
				monto=datos_prestamo['monto'],
				tasa_interes_anual=datos_prestamo['tasa_interes_anual'],
				plazo_meses=datos_prestamo['plazo_meses'],
				estado='Pendiente'
			)
			decision = evaluar_prestamo(solicitante, nuevo_prestamo)
			logger.info(f"Resultado de decisión para solicitud {solicitud_id}: {decision}")

			plan_pago = None
			if decision == Decision.APROBADO:
				getcontext().prec = 28
				getcontext().rounding = ROUND_HALF_UP
				plan_pago = []
				saldo = Decimal(str(nuevo_prestamo.monto))
				tasa_mensual = Decimal(str(nuevo_prestamo.tasa_interes_anual)) / Decimal('12')
				cuota = Decimal(str(nuevo_prestamo.cuota_mensual()))
				for n in range(1, nuevo_prestamo.plazo_meses + 1):
					interes = saldo * tasa_mensual
					abono_capital = cuota - interes
					plan_pago.append({
						"numero_cuota": n,
						"cuota": str(cuota.quantize(Decimal('0.01'))),
						"abono_capital": str(abono_capital.quantize(Decimal('0.01'))),
						"interes": str(interes.quantize(Decimal('0.01'))),
						"saldo_restante": str(max(saldo - abono_capital, Decimal('0')).quantize(Decimal('0.01')))
					})
					saldo -= abono_capital

			ok, error_msg = self.repository.actualizar_estado_solicitud(
				solicitud_id, decision, plan_pago=plan_pago,
				monto=datos_prestamo['monto'],
				tasa_interes=datos_prestamo['tasa_interes_anual'],
				plazo=datos_prestamo['plazo_meses']
			)
			if not ok:
				logger.error(f"Fallo al actualizar estado: {error_msg}")
				return {"error": f"No se pudo actualizar el estado de la solicitud: {error_msg}"}
			result = {"solicitud_id": solicitud_id, "decision": decision}
			if plan_pago is not None:
				result["plan_pago"] = plan_pago
			return result
		except Exception as e:
			logger.error(f"Error en cálculo de capacidad para solicitud {solicitud_id}: {str(e)}", exc_info=True)
			return {"error": "No se pudo procesar la solicitud. Intente más tarde."}
