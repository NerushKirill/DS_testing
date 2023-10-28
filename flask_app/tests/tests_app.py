import pytest
from redis import StrictRedis
from ..app.main import app


@pytest.fixture(scope='module')
def test_app():
    return app.test_client()


@pytest.fixture(scope='module')
def test_redis():
    return StrictRedis(host='localhost', port=6379, db=0)


def test_root(test_app):
    response = test_app.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": 200}


def test_create_key_value(test_app, test_redis):
    payload = {
        "key": "test_key",
        "value": "test_value"
    }
    response = test_app.post('/create', json=payload)
    assert response.status_code == 200
    assert response.get_json() == {"message": "Key-Value pair created successfully"}
    value = test_redis.get("test_key")
    assert value.decode('utf-8') == "test_value"


def test_read_key_value(test_app, test_redis):
    test_redis.set("test_key", "test_value")
    response = test_app.get('/read/test_key')
    assert response.status_code == 200
    assert response.get_json() == {"test_key": "test_value"}


def test_read_key_value_not_found(test_app, test_redis):
    response = test_app.get('/read/nonexistent_key')
    assert response.status_code == 200
    assert response.get_json() == {"nonexistent_key": None}


def test_update_key_value(test_app, test_redis):
    test_redis.set("test_key", "test_value")
    payload = {
        "key": "test_key",
        "value": "updated_value"
    }
    response = test_app.put('/update', json=payload)
    assert response.status_code == 200
    assert response.get_json() == {"message": "Key-Value pair updated successfully"}
    value = test_redis.get("test_key")
    assert value.decode('utf-8') == "updated_value"


def test_delete_key(test_app, test_redis):
    test_redis.set("test_key", "test_value")
    response = test_app.delete('/delete/test_key')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Key 'test_key' successfully deleted"}
    value = test_redis.get("test_key")
    assert value is None


def test_delete_key_not_found(test_app, test_redis):
    response = test_app.delete('/delete/nonexistent_key')
    assert response.status_code == 404
    assert response.get_json() == {"message": "Key 'nonexistent_key' not found"}


def test_receive_alert(test_app, capsys):
    payload = {
        "message": "Test alert"
    }
    response = test_app.post('/alert', json=payload)
    assert response.status_code == 200
    assert response.get_json() == {"message": "Alert received"}
    captured = capsys.readouterr()
    assert "Received alert: Test alert" in captured.out
