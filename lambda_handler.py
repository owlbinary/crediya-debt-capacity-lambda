import os
import json
from dotenv import load_dotenv
load_dotenv()

def lambda_handler(event, context):
    """
    Handler para AWS Lambda con trigger SQS. Procesa mensajes de capacidad de endeudamiento.
    Mantiene la misma lógica que el endpoint FastAPI /api/v1/calcular-capacidad
    """
    from app.application.capacidad_service import CapacidadEndeudamientoService
    from app.infrastructure.repository import Repository
    from app.infrastructure.logger import get_logger
    from app.domain.exceptions import SolicitudNoActualizableException
    import logging

    logger = get_logger()
    service = CapacidadEndeudamientoService(Repository())
    
    for record in event.get("Records", []):
        try:
            body = record["body"]
            try:
                request_data = json.loads(body) if isinstance(body, str) else body
            except json.JSONDecodeError as json_error:
                logger.error(f"Error al parsear el mensaje JSON: {json_error}")
                continue
            
            logger.info(f"Procesando mensaje de capacidad de endeudamiento: {request_data}")
            
            solicitud_id = request_data.get("solicitudId")
            salario = request_data.get("salarioBase")
            ingresos_totales = salario
            tipo_prestamo = request_data.get("tipoPrestamo") or {}
            tasa_interes = tipo_prestamo.get("tasaInteres")
            plazo = request_data.get("plazo")
            monto = request_data.get("monto")
            documento_identidad = request_data.get("documentoIdentidad")
            deuda_total_mensual = request_data.get("deudaTotalMensual")

            if not tasa_interes:
                logger.warning("Datos incompletos en la solicitud (tasaInteres)")
                continue

            datos_solicitante = {
                "id": documento_identidad,
                "ingresos_totales": ingresos_totales,
                "salario": salario,
                "deuda_total_mensual": deuda_total_mensual
            }
            datos_prestamo = {
                "monto": monto,
                "tasa_interes_anual": tasa_interes,
                "plazo_meses": plazo,
            }

            resultado = service.calcular_y_actualizar_estado(
                solicitud_id, datos_solicitante, datos_prestamo
            )
            
            if isinstance(resultado, dict) and ("mensaje" in resultado or "error" in resultado) and not resultado.get("decision"):
                mensaje = resultado.get("mensaje") or resultado.get("error")
                codigo = resultado.get("codigo") or "ESTADO_SOLICITUD_NO_VALIDO"
                logger.error(f"Error en solicitud {solicitud_id}: {mensaje} (Código: {codigo})")
                continue
            
            logger.info(f"Capacidad calculada exitosamente para solicitud {solicitud_id}: {resultado}")
            
        except SolicitudNoActualizableException as solicitud_error:
            logger.error(f"Error de solicitud no actualizable: {solicitud_error}")
        except Exception as e:
            logger.error(f"Error inesperado procesando mensaje SQS: {e}")
    
    return {"statusCode": 200, "message": "Procesamiento completado"}
