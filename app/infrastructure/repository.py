from app.infrastructure.logger import get_logger
import os
import json
import boto3
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

class Repository:
	def __init__(self):
		self.logger = get_logger()
		self.debt_capacity_queue_url = os.getenv('SQS_DEBT_CAPACITY_QUEUE_URL')
		self.state_queue_url = os.getenv('SQS_STATE_QUEUE_URL')

		self.logger.info(f"Inicializando Repository con debt_capacity_queue_url: {self.debt_capacity_queue_url}")
		self.logger.info(f"Inicializando Repository con state_queue_url: {self.state_queue_url}")

		self.sqs_client = boto3.client(
			'sqs',
			region_name=os.getenv('AWS_REGION', 'us-east-1')
		)

	def actualizar_estado_solicitud(self, solicitud_id: str, nuevo_estado: str, plan_pago=None):
		"""
		Envía un mensaje a SQS para que el microservicio de applications 
		procese la actualización de estado de forma asíncrona
		"""
		try:
			if not self.state_queue_url:
				error_msg = "SQS_STATE_QUEUE_URL no está configurada"
				self.logger.error(error_msg)
				return False, error_msg
			
			message_body = {
				"tipo": "actualizar_estado_solicitud",
				"timestamp": datetime.now(timezone.utc).isoformat(),
				"params": {
					"solicitudId": solicitud_id,
					"nuevoEstado": nuevo_estado,
					"justificacion": "Procesado por validación automática de capacidad de endeudamiento",
					"origen": "debt-capacity-lambda"
				}
			}
			
			if plan_pago is not None:
				message_body["params"]["planPago"] = plan_pago
			
			response = self.sqs_client.send_message(
				QueueUrl=self.state_queue_url,
				MessageBody=json.dumps(message_body),
				MessageAttributes={
					'tipo': {
						'StringValue': 'actualizar_estado_solicitud',
						'DataType': 'String'
					},
					'solicitudId': {
						'StringValue': solicitud_id,
						'DataType': 'String'
					}
				}
			)
			
			self.logger.info(f"Mensaje enviado a SQS para actualizar solicitud {solicitud_id} a estado {nuevo_estado}. MessageId: {response['MessageId']}")
			return True, None
			
		except Exception as e:
			self.logger.error(f"Error al enviar mensaje SQS para solicitud {solicitud_id}: {str(e)}", exc_info=True)
			return False, str(e)