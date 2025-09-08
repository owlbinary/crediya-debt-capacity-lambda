from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from datetime import datetime
from app.domain.schemas import ErrorResponse
from app.domain.exceptions import SolicitudNoActualizableException

def register_exception_handlers(app):
    @app.exception_handler(SolicitudNoActualizableException)
    async def solicitud_no_actualizable_handler(request: Request, exc: SolicitudNoActualizableException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorResponse(
                codigo=exc.codigo,
                mensaje=exc.detalle,
                timestamp=datetime.now().isoformat(),
                path=request.url.path
            ).dict()
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                codigo="VALIDATION_ERROR",
                mensaje="Error de validación",
                timestamp=datetime.now().isoformat(),
                path=request.url.path,
                detalles=exc.errors()
            ).dict()
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                codigo="HTTP_ERROR",
                mensaje=exc.detail,
                timestamp=datetime.now().isoformat(),
                path=request.url.path
            ).dict()
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                codigo="ERROR_INTERNO",
                mensaje="Error interno. Intente más tarde.",
                timestamp=datetime.now().isoformat(),
                path=request.url.path
            ).dict()
        )
