import requests

API_URL = "http://127.0.0.1:5000"


def buscar_questoes_iniciais():
    try:
        response = requests.get(f"{API_URL}/play/questions/initial")
        response.raise_for_status()

        dados_api = response.json()
        perguntas = []

        for q in dados_api:
            opcoes = [resp["text"] for resp in q["responses"]]

            perguntas.append({
                "idQuestion": q["id"],
                "titulo": f"Questão: {q.get('dsTheme', 'Conhecimento')}",
                "pergunta": q["question"],
                "opcoes": opcoes,
                "resposta_correta": q["correctAnswer"],
                "pontos": 10
            })

        return perguntas

    except Exception as erro:
        print(f"[API][QUESTÕES] Erro ao buscar questões: {erro}")
        return []