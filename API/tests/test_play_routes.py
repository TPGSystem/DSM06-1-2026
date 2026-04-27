import pytest
import json

def test_fluxo_completo_gameplay(client):
    # 1. TESTE DE LOGIN (Usando seus dados do Seed)
    login_payload = {
        "ra": "000001", 
        "password": "111"
    }
    response = client.post('/play/login', json=login_payload)
    
    # Se falhar aqui, o erro 401 aparecerá. Com os dados acima, deve retornar 200.
    assert response.status_code == 200
    data = response.get_json()
    assert data['authenticated'] is True
    
    student_id = data['student']['id']
    class_id = data['class']['id']

    # 2. TESTE DE SELEÇÃO DE PERSONAGEM
    # Certifique-se de que o idCharacter 1 existe no seu seeder de personagens
    select_payload = {
        "idStudent": student_id,
        "idClass": class_id,
        "idCharacter": 1, 
        "matchName": "Jornada de Teste"
    }
    response = client.post('/play/select-character', json=select_payload)
    assert response.status_code == 201
    match_data = response.get_json()
    
    # Ajuste aqui conforme a estrutura de retorno do seu controller
    # Se retornar {'match': {'id': ...}}
    match_id = match_data['match']['id'] if 'match' in match_data else match_data['idMatch']
    assert match_id is not None

    # 3. TESTE DE BUSCA DE QUESTÕES (ALGORITMO ABC)
    response = client.get(f'/play/questions/smart/{student_id}/{class_id}?region=1')
    assert response.status_code == 200
    questions = response.get_json()
    assert len(questions) == 5

    # 4. TESTE DE SALVAMENTO DE QUESTÕES
    save_qs_payload = {
        "idGameMatch": match_id,
        "idRegion": 1,
        "answers": [
            {"idQuestion": questions[0]['id'], "points": 10},
            {"idQuestion": questions[1]['id'], "points": 10},
            {"idQuestion": questions[2]['id'], "points": 10},
            {"idQuestion": questions[3]['id'], "points": 10},
            {"idQuestion": questions[4]['id'], "points": 10}
        ]
    }
    response = client.post('/play/save-questions', json=save_qs_payload)
    assert response.status_code == 201
    step_id = response.get_json()['idStep']

    # 5. TESTE DE DESAFIO FINAL
    save_chall_payload = {
        "idStep": step_id,
        "points": 50,
        "number": 1  
    }
    response = client.post('/play/save-challenge', json=save_chall_payload)
    assert response.status_code == 200
    assert "idGamesChallenge" in response.get_json() or "message" in response.get_json()

def test_login_falha_ra_inexistente(client):
    payload = {"ra": "999999", "password": "111"}
    response = client.post('/play/login', json=payload)
    assert response.status_code == 401
    
def test_status_regioes(client):
    # Usando um ID fictício para validar apenas a estrutura da rota
    response = client.get('/play/regions/status/1')
    assert response.status_code in [200, 404]
    