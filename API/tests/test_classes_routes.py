import pytest

@pytest.fixture
def class_data(client):
    # Arrange
    payload = {
        "schoolYear": 2026,
        "idYearSerie": 1,
        "idComponent": 1,
        "idTeacher": 1
    }
    response = client.post('/classes', json=payload)
    return response.json

def test_class_create_success(client):
    # Arrange
    body = {
        "schoolYear": 2026,
        "idYearSerie": 1, 
        "idComponent": 1,
        "idTeacher": 1
    }

    # Act
    response = client.post('/classes', json=body)

    # Assert
    assert response.status_code == 201
    assert response.json['schoolYear'] == 2026
    assert 'id' in response.json

def test_class_create_fail_missing_field(client):
    # Arrange
    body = { "schoolYear": 2026 } # Faltam campos obrigatórios

    # Act
    response = client.post('/classes', json=body)

    # Assert
    assert response.status_code == 400
    assert 'error' in response.json

def test_class_list_and_get(client, class_data):
    # Act (Listagem Geral)
    response_list = client.get('/classes')

    # Assert
    assert response_list.status_code == 200
    assert isinstance(response_list.json, list)

    # Act (Busca Individual)
    class_id = class_data['id']
    response_get = client.get(f'/classes/{class_id}')

    # Assert
    assert response_get.status_code == 200
    assert response_get.json['id'] == class_id

def test_class_list_by_teacher(client, class_data):
    # Arrange
    teacher_id = class_data['idTeacher']

    # Act
    response = client.get(f'/classes/teacher/{teacher_id}')

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert any(c['id'] == class_data['id'] for c in response.json)

def test_class_update_success(client, class_data):
    # Arrange
    class_id = class_data['id']
    body = { "schoolYear": 2027 }

    # Act
    response = client.put(f'/classes/{class_id}', json=body)

    # Assert
    assert response.status_code == 200
    assert response.json['schoolYear'] == 2027

def test_class_delete_not_found(client):
    # Arrange
    invalid_id = 9999

    # Act
    response = client.delete(f'/classes/{invalid_id}')

    # Assert
    assert response.status_code == 404
    assert response.json['message'] == "Registro Não Encontrado"
    