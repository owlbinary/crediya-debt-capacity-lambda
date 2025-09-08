import pytest
from app.domain import exceptions
from fastapi import status

def test_solicitud_no_actualizable_exception():
    ex = exceptions.SolicitudNoActualizableException("No se puede actualizar", codigo="CODIGO_X")
    assert ex.detalle == "No se puede actualizar"
    assert ex.codigo == "CODIGO_X"
    ex2 = exceptions.SolicitudNoActualizableException("Otro error")
    assert ex2.codigo == "ESTADO_SOLICITUD_NO_VALIDO"

def test_error_de_validacion():
    detalles = [{"loc": ["body", "campo"], "msg": "falta"}]
    ex = exceptions.ErrorDeValidacion(detalles)
    assert ex.detalles == detalles
    assert ex.codigo == "VALIDATION_ERROR"
    assert ex.mensaje == "Error de validación"
    assert ex.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_error_http():
    ex = exceptions.ErrorHTTP("Mensaje", 404)
    assert ex.codigo == "HTTP_ERROR"
    assert ex.mensaje == "Mensaje"
    assert ex.status_code == 404

def test_error_interno():
    ex = exceptions.ErrorInterno()
    assert ex.codigo == "ERROR_INTERNO"
    assert ex.mensaje == "Error interno. Intente más tarde."
    assert ex.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    ex2 = exceptions.ErrorInterno("Otro error")
    assert ex2.mensaje == "Otro error"
