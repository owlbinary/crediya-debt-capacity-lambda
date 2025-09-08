from app.infrastructure.logger import get_logger
import os
import requests
from dotenv import load_dotenv
load_dotenv()

class Repository:
	def __init__(self):
		self.logger = get_logger()

	def actualizar_estado_solicitud(self, solicitud_id: str, nuevo_estado: str, jwt_token: str = None, plan_pago=None):
		base_url = os.getenv("BASE_URL_SERVICIO_SOLICITUDES", "http://localhost:8080")
		url = f"{base_url}/api/v1/solicitudes/{solicitud_id}"
		body = {
			"nuevoEstado": nuevo_estado,
			"justificacion": "Aprobado por validación automática",
			"planPago": plan_pago if plan_pago is not None else None
		}
		headers = {}
		if jwt_token:
			headers["Authorization"] = f"Bearer {jwt_token}"
		try:
			response = requests.patch(url, json=body, headers=headers, timeout=5)
			response.raise_for_status()
			self.logger.info(f"Estado actualizado para solicitud {solicitud_id}: {nuevo_estado}")
			return True, None
		except Exception as e:
			self.logger.error(f"Error al actualizar estado para solicitud {solicitud_id}: {str(e)}", exc_info=True)
			return False, str(e)