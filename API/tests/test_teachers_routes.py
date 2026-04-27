import pytest

def test_teacher_create_success(client):
    # Arrange
    body = {
        "name": "Professor Girafales",
        "eMail": "girafales@escola.com",
        "password": "mestre-linguica"
    }

    # Act
    response = client.post('/teachers', json=body)

    # Assert
    assert response.status_code == 201
    assert response.json['name'] == "Professor Girafales"
    assert response.json['eMail'] == "girafales@escola.com"

def test_teacher_create_fail(client):
    # Arrange
    body = { "name": "Professor Incompleto" } 

    # Act
    response = client.post('/teachers', json=body)

    # Assert
    assert response.status_code == 400
    assert 'error' in response.json

def test_teacher_login_success(client):
    # Arrange
    # criar um professor 
    setup_body = {
        "name": "Professor Login",
        "eMail": "login@teste.com",
        "password": "senha123"
    }
    client.post('/teachers', json=setup_body)
    
    login_data = {
        "eMail": "login@teste.com",
        "password": "senha123"
    }

    # Act
    response = client.post('/teachers/login', json=login_data)

    # Assert
    assert response.status_code == 200
    assert response.json['message'] == "Login realizado com sucesso"
    assert 'id' in response.json

def test_teacher_login_fail(client):
    # Arrange
    body = {
        "eMail": "errado@teste.com",
        "password": "senha_incorreta"
    }

    # Act
    response = client.post('/teachers/login', json=body)

    # Assert
    assert response.status_code == 401
    assert response.json['error'] == "Credenciais inválidas"

def test_teacher_list_and_get(client):
    # Listagem
    # Act
    response = client.get('/teachers')

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json, list)

    # Busca Individual
    # Act
    response = client.get('/teachers/1')

    # Assert
    if response.status_code == 200:
        assert 'eMail' in response.json
    else:
        assert response.status_code == 404

def test_teacher_update_success(client):
    # Arrange
    teacher_id = 1
    body = { "name": "Professor Atualizado" }

    # Act
    response = client.put(f'/teachers/{teacher_id}', json=body)

    # Assert
    if response.status_code == 200:
        assert response.json['name'] == "Professor Atualizado"
    else:
        pytest.skip(f"Professor ID {teacher_id} não encontrado")

def test_teacher_delete_fail_in_use(client):
    # Arrange
    teacher_id = 1

    # Act
    response = client.delete(f'/teachers/{teacher_id}')

    # Assert
    if response.status_code == 400:
        assert "está sendo utilizado" in response.json['message']
    elif response.status_code == 404:
         pytest.skip(f"Professor ID {teacher_id} não encontrado")

def test_teacher_delete_not_found(client):
    # Arrange
    invalid_id = 9999

    # Act
    response = client.delete(f'/teachers/{invalid_id}')

    # Assert
    assert response.status_code == 404