import json
from unittest.mock import patch

from ..app.main import app


def test_create_key_value():
    with patch('app.request') as mock_request:
        mock_request.get_json.return_value = {'key': 'test_key', 'value': 'test_value'}
        response = app.test_client().post('/create')
        assert response.status_code == 200
        assert json.loads(response.data) == {"message": "Key-Value pair created successfully"}


def test_read_key_value():
    with patch('app.redis_client') as mock_redis:
        mock_redis.get.return_value = b'test_value'
        response = app.test_client().get('/read/test_key')
        assert response.status_code == 200
        assert json.loads(response.data) == {'test_key': 'test_value'}


def test_update_key_value():
    with patch('app.request') as mock_request, patch('app.redis_client') as mock_redis:
        mock_request.get_json.return_value = {'key': 'test_key', 'value': 'new_test_value'}
        response = app.test_client().put('/update')
        assert response.status_code == 200
        assert json.loads(response.data) == {"message": "Key-Value pair updated successfully"}


def test_delete_key():
    with patch('app.redis_client') as mock_redis:
        mock_redis.delete.return_value = 1
        response = app.test_client().delete('/delete/test_key')
        assert response.status_code == 200
        assert json.loads(response.data) == {"message": "Key 'test_key' successfully deleted"}


def test_receive_alert():
    with patch('app.request') as mock_request:
        mock_request.get_json.return_value = {'message': 'test_alert'}
        with patch('builtins.print') as mock_print:
            response = app.test_client().post('/alert')
            assert response.status_code == 200
            assert json.loads(response.data) == {"message": "Alert received"}
            mock_print.assert_called_once_with("Received alert: test_alert")
