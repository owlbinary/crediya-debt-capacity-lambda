from app.infrastructure.repository import Repository
from unittest.mock import patch, MagicMock
import json
import os


def test_repository_init():
    """Test Repository initialization"""
    with patch.dict(os.environ, {'SQS_STATE_QUEUE_URL': 'test-queue-url'}):
        repo = Repository()
        assert hasattr(repo, 'logger')
        assert hasattr(repo, 'sqs_client')
        assert repo.state_queue_url == 'test-queue-url'


@patch("app.infrastructure.repository.boto3.client")
def test_actualizar_estado_solicitud_success(mock_boto_client):
    """Test successful message sending to SQS"""
    mock_sqs = MagicMock()
    mock_sqs.send_message.return_value = {'MessageId': 'test-message-id'}
    mock_boto_client.return_value = mock_sqs
    
    with patch.dict(os.environ, {'SQS_STATE_QUEUE_URL': 'test-queue-url'}):
        repo = Repository()
        success, error = repo.actualizar_estado_solicitud("123", "APROBADO")
        
        assert success is True
        assert error is None
        mock_sqs.send_message.assert_called_once()
        
        call_args = mock_sqs.send_message.call_args
        message_body = json.loads(call_args[1]['MessageBody'])
        assert message_body['tipo'] == 'actualizar_estado_solicitud'
        assert message_body['params']['solicitudId'] == '123'
        assert message_body['params']['nuevoEstado'] == 'APROBADO'


@patch("app.infrastructure.repository.boto3.client")
def test_actualizar_estado_solicitud_with_plan_pago(mock_boto_client):
    """Test message sending with plan de pago"""
    mock_sqs = MagicMock()
    mock_sqs.send_message.return_value = {'MessageId': 'test-message-id'}
    mock_boto_client.return_value = mock_sqs
    
    plan_pago = [{"numero_cuota": 1, "cuota": "1000.00"}]
    
    with patch.dict(os.environ, {'SQS_STATE_QUEUE_URL': 'test-queue-url'}):
        repo = Repository()
        success, error = repo.actualizar_estado_solicitud("123", "APROBADO", plan_pago=plan_pago)
        
        assert success is True
        assert error is None
        
        call_args = mock_sqs.send_message.call_args
        message_body = json.loads(call_args[1]['MessageBody'])
        assert 'planPago' in message_body['params']
        assert message_body['params']['planPago'] == plan_pago


@patch("app.infrastructure.repository.boto3.client")
def test_actualizar_estado_solicitud_no_queue_url(mock_boto_client):
    """Test error when queue URL is not configured"""
    mock_sqs = MagicMock()
    mock_boto_client.return_value = mock_sqs
    
    with patch.dict(os.environ, {}, clear=True):
        repo = Repository()
        success, error = repo.actualizar_estado_solicitud("123", "APROBADO")
        
        assert success is False
        assert "SQS_STATE_QUEUE_URL no está configurada" in error
        mock_sqs.send_message.assert_not_called()


@patch("app.infrastructure.repository.boto3.client")
def test_actualizar_estado_solicitud_sqs_error(mock_boto_client):
    """Test SQS sending error handling"""
    mock_sqs = MagicMock()
    mock_sqs.send_message.side_effect = Exception("SQS error")
    mock_boto_client.return_value = mock_sqs
    
    with patch.dict(os.environ, {'SQS_STATE_QUEUE_URL': 'test-queue-url'}):
        repo = Repository()
        success, error = repo.actualizar_estado_solicitud("123", "APROBADO")
        
        assert success is False
        assert "SQS error" in error
