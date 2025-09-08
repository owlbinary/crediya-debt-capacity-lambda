from fastapi import status

class SolicitudNoActualizableException(Exception):
    def __init__(self, detalle: str, codigo: str = None):
        self.detalle = detalle
        self.codigo = codigo or "ESTADO_SOLICITUD_NO_VALIDO"

class ErrorDeValidacion(Exception):
    def __init__(self, detalles):
        self.detalles = detalles
        self.codigo = "VALIDATION_ERROR"
        self.mensaje = "Error de validación"
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

class ErrorHTTP(Exception):
    def __init__(self, mensaje, status_code):
        self.codigo = "HTTP_ERROR"
        self.mensaje = mensaje
        self.status_code = status_code

class ErrorInterno(Exception):
    def __init__(self, mensaje="Error interno. Intente más tarde."):
        self.codigo = "ERROR_INTERNO"
        self.mensaje = mensaje
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
