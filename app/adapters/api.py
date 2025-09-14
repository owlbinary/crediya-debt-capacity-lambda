
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse
from app.application.capacidad_service import CapacidadEndeudamientoService
from app.infrastructure.repository import Repository
from app.infrastructure.logger import get_logger
from app.domain.exceptions import SolicitudNoActualizableException
from app.domain.exception_handlers import register_exception_handlers
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from app.domain.schemas import ErrorResponse
from datetime import datetime
from fastapi import Body
from app.domain.capacidad_schemas import CalcularCapacidadRequest, CalcularCapacidadResponse

app = FastAPI()
register_exception_handlers(app)
logger = get_logger()
service = CapacidadEndeudamientoService(Repository())

@app.post("/api/v1/calcular-capacidad", response_model=CalcularCapacidadResponse)
async def calcular_capacidad(request_data: CalcularCapacidadRequest = Body(...)):
    solicitud_id = request_data.solicitudId
    salario = request_data.salarioBase
    ingresos_totales = salario
    tipo_prestamo = request_data.tipoPrestamo or {}
    tasa_interes = tipo_prestamo.get("tasaInteres")
    plazo = request_data.plazo
    monto = request_data.monto
    documento_identidad = request_data.documentoIdentidad
    deuda_total_mensual = request_data.deudaTotalMensual

    if not tasa_interes:
        logger.warning("Datos incompletos en la solicitud (tasaInteres)")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Datos incompletos: tasaInteres")

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
        raise SolicitudNoActualizableException(mensaje, codigo)
    return resultado