from app.infrastructure.repository import Repository
from unittest.mock import patch, MagicMock

def test_repository_init():
    repo = Repository()
    assert hasattr(repo, 'logger')

def test_actualizar_estado_solicitud():
    repo = Repository()
    repo.actualizar_estado_solicitud('sol1', 'APROBADO')

@patch("app.infrastructure.repository.requests.patch")
def test_actualizar_estado_solicitud_envia_patch(mock_patch):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_patch.return_value = mock_response
    repo = Repository()
    repo.actualizar_estado_solicitud("123", "APROBADO", jwt_token="token123")
    mock_patch.assert_called_once()
    _, kwargs = mock_patch.call_args
    assert "Authorization" in kwargs["headers"]
    assert kwargs["headers"]["Authorization"] == "Bearer token123"
    assert kwargs["json"]["nuevoEstado"] == "APROBADO"
    assert kwargs["timeout"] == 5

@patch("app.infrastructure.repository.requests.patch")
def test_actualizar_estado_solicitud_sin_token(mock_patch):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_patch.return_value = mock_response
    repo = Repository()
    repo.actualizar_estado_solicitud("123", "RECHAZADO")
    _, kwargs = mock_patch.call_args
    assert "Authorization" not in kwargs["headers"]
    assert kwargs["json"]["nuevoEstado"] == "RECHAZADO"

@patch("app.infrastructure.repository.requests.patch")
def test_actualizar_estado_solicitud_error_log(mock_patch):
    mock_patch.side_effect = Exception("fail")
    repo = Repository()
    repo.actualizar_estado_solicitud("123", "APROBADO", jwt_token="token123")
