import pytest

@pytest.fixture
def character_data(client):
    # Arrange
    response = client.get('/characters')
    if response.status_code == 200 and len(response.json) > 0:
        return response.json[0]
    return None

def test_character_list_and_get(client, character_data):
    # Act (Listagem)
    response = client.get('/characters')

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json, list)

    # Act (Busca Individual)
    if character_data:
        char_id = character_data['id']
        response_get = client.get(f'/characters/{char_id}')

        # Assert
        assert response_get.status_code == 200
        assert response_get.json['id'] == char_id
        assert 'scoreStrength' in response_get.json

def test_character_get_not_found(client):
    # Arrange
    invalid_id = 9999

    # Act
    response = client.get(f'/characters/{invalid_id}')

    # Assert
    assert response.status_code == 404
    assert response.json['message'] == "Registro Não Encontrado"
    