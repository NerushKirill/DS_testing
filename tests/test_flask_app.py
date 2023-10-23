import httpx


BASE_URL = 'http://localhost:8080'


def test_create_key_value():
    response = httpx.post(f'{BASE_URL}/create', json={'key': 'test_key', 'value': 'test_value'})
    assert response.status_code == 200
    assert response.json() == {"message": "Key-Value pair created successfully"}


def test_read_key_value():
    key = 'test_key'
    value = 'test_value'
    httpx.post(f'{BASE_URL}/create', json={'key': key, 'value': value})
    response = httpx.get(f'{BASE_URL}/read/{key}')
    assert response.status_code == 200
    assert response.json() == {key: value}


def test_update_key_value():
    key = 'test_key'
    value = 'new_test_value'
    httpx.post(f'{BASE_URL}/create', json={'key': key, 'value': 'test_value'})
    response = httpx.put(f'{BASE_URL}/update', json={'key': key, 'value': value})
    assert response.status_code == 200
    assert response.json() == {"message": "Key-Value pair updated successfully"}
    response = httpx.get(f'{BASE_URL}/read/{key}')
    assert response.json() == {key: value}


def test_delete_key():
    key = 'test_key'
    httpx.post(f'{BASE_URL}/create', json={'key': key, 'value': 'test_value'})
    response = httpx.delete(f'{BASE_URL}/delete/{key}')
    assert response.status_code == 200
    assert response.json() == {"message": f"Key '{key}' successfully deleted"}
    response = httpx.get(f'{BASE_URL}/read/{key}')
    assert response.json() == {key: None}


def test_receive_alert():
    response = httpx.post(f'{BASE_URL}/alert', json={'message': 'test_alert'})
    assert response.status_code == 200
    assert response.json() == {"message": "Alert received"}
