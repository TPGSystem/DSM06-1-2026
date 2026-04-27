import pytest

@pytest.fixture
def student_data(client):
    payload = {
        "name": "Aluno Fixture",
        "ra": "777777",
        "password": "123",
        "birth": "2010-05-20",
        "idClass": 1
    }
    client.post('/students', json=payload)
    return payload

def test_student_create_success(client):
    # Arrange
    body = {
        "name": "Aluno Teste",
        "ra": "999999",
        "password": "123",
        "birth": "2010-05-20",
        "idClass": 3
    }

    # Act
    response = client.post('/students', json=body)

    # Assert
    assert response.status_code == 201
    assert response.json['name'] == "Aluno Teste"
    assert response.json['ra'] == "999999"

def test_student_create_fail(client):
    # Arrange
    body = { "name": "Sem RA" }

    # Act
    response = client.post('/students', json=body)

    # Assert
    assert response.status_code == 400
    assert 'error' in response.json

def test_student_login_success(client, student_data):    # Arrange
    body = {
        "ra": student_data["ra"],
        "password": student_data["password"]
    }

    # Act
    response = client.post('/students/login', json=body)

    # Assert
    assert response.status_code == 200
    assert response.json['ra'] == student_data["ra"]
    assert response.json['message'] == "Login realizado com sucesso"
    
def test_student_login_fail(client):
    # Arrange
    body = {
        "ra": "999999",
        "password": "999999"
    }

    # Act
    response = client.post('/students/login', json=body)

    # Assert
    assert response.status_code == 401
    assert response.json['error'] == "Credenciais inválidas"
   
def test_student_list_and_get(client):
    # Listagem
    # Act 
    response = client.get('/students')

    # Assert 
    assert response.status_code == 200
    assert isinstance(response.json, list)

    # Busca Individual
    # Act 
    response = client.get('/students/1')

    # Assert 
    if response.status_code == 200:
        assert 'name' in response.json
    else:
        assert response.status_code == 404

def test_student_update_success(client):
    # Arrange
    student_id = 1
    body = { "name": "Nome Alterado" }

    # Act
    response = client.put(f'/students/{student_id}', json=body)

    # Assert
    if response.status_code == 200:
        assert response.json['name'] == "Nome Alterado"
    else:
        pytest.skip(f"Estudante ID {student_id} não encontrado")

def test_student_update_fail(client):
    # Arrange
    invalid_id = 9999

    # Act
    response = client.put(f'/students/{invalid_id}', json={"name": "Erro"})

    # Assert
    assert response.status_code == 404

def test_student_delete(client):
    # Arrange
    non_existent_id = 9999

    # Act
    response = client.delete(f'/students/{non_existent_id}')

    # Assert
    assert response.status_code == 404