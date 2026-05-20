import requests

API_URL = "http://127.0.0.1:5000"


def login(ra, password):
    try:
        response = requests.post(
            f"{API_URL}/play/login",
            json={
                "ra": ra,
                "password": password
            },
            timeout=5
        )

        return response.json()

    except Exception as e:
        print(f"Erro na API: {e}")
        return None


def select_character(student_id, class_id, character_id):
    try:
        response = requests.post(
            f"{API_URL}/play/select-character",
            json={
                "idStudent": student_id,
                "idClass": class_id,
                "idCharacter": character_id,
                "matchName": "Partida Teste"
            },
            timeout=5
        )

        print("[API][select_character] Status:", response.status_code)
        print("[API][select_character] Texto:", response.text)

        if response.status_code in (200, 201):
            return response.json()

        return None

    except Exception as e:
        print(f"Erro ao selecionar personagem: {e}")
        return None

def save_challenge(id_step, points, number):
    try:
        response = requests.post(
            f"{API_URL}/play/save-challenge",
            json={
                "idStep": id_step,
                "points": points,
                "number": number
            },
            timeout=5
        )

        print("[API][save_challenge] Status:", response.status_code)
        print("[API][save_challenge] Texto:", response.text)

        if response.status_code in (200, 201):
            return response.json()

        return None

    except Exception as e:
        print(f"Erro ao salvar desafio: {e}")
        return None

def save_questions(id_game_match, id_region, answers):
    try:
        response = requests.post(
            f"{API_URL}/play/save-questions",
            json={
                "idGameMatch": id_game_match,
                "idRegion": id_region,
                "answers": answers
            },
            timeout=5
        )

        print("[API][save_questions] Status:", response.status_code)
        print("[API][save_questions] Texto:", response.text)

        if response.status_code in (200, 201):
            return response.json()

        return None

    except Exception as e:
        print(f"Erro ao salvar questões: {e}")
        return None

