def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == 'OK'


def test_get_protection_system(client):
    response = client.get('/protection_systems/1')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['id'] == 1


def test_get_device(client):
    response = client.get('/devices/1')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['id'] == 1


def test_get_content(client):
    response = client.get('/contents/1')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['id'] == 1


def test_get_decrypted_content(client):
    response = client.get('/get_content?content_id=1&device_id=1')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'OK'


def test_create_protection_system(client):
    payload = {
        'name': 'AES 2',
        'encryption_mode': "AES + CCM"
    }
    response = client.post('/protection_systems', json=payload)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['status'] == 'OK'


def test_create_device(client):
    payload = {
        'name': 'Samsung',
        'protection_system_id': 2
    }
    response = client.post('/devices', json=payload)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['status'] == 'OK'


def test_create_content(client):
    payload = {
        'content_payload': 'This is the text to be encrypted.',
        'protection_system_id': 2
    }
    response = client.post('/contents', json=payload)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['status'] == 'OK'


def test_get_decrypted_content_401(client):
    response = client.get('/get_content?content_id=2&device_id=1')
    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data['status'] == 'Error'
