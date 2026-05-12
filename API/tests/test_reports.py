import pytest

# Fixture para centralizar os parâmetros comuns de teste
@pytest.fixture
def report_params():
    return {
        "teacher_id": 1,
        "year": 2026,
        "class_id": 1,
        "student_id": 1,
        "theme_id": 1
    }

def test_report_performance_success(client, report_params):
    # Act: Testa performance geral do professor
    url = f"/reports/performance?teacher_id={report_params['teacher_id']}&year={report_params['year']}"
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert "by_theme" in response.json
    assert "general_summary" in response.json
    assert isinstance(response.json['by_theme'], list)

def test_report_engagement_success(client, report_params):
    # Act: Testa relatório de engajamento (alunos ativos/inativos)
    url = f"/reports/engagement?teacher_id={report_params['teacher_id']}&year={report_params['year']}"
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert "totals" in response.json
    assert "summary_by_class" in response.json
    assert "details" in response.json

def test_report_top_errors_with_difficulty(client, report_params):
    # Act: Testa questões críticas filtrando por turma (para trazer dificuldade)
    url = (f"/reports/top-errors?teacher_id={report_params['teacher_id']}"
           f"&year={report_params['year']}&class_id={report_params['class_id']}")
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    if len(response.json) > 0:
        assert "difficulty" in response.json[0]
        assert "question_text" in response.json[0]

def test_report_evolution_with_regua(client, report_params):
    # Act: Testa evolução mensal com filtro de aluno e régua (meta)
    url = (f"/reports/evolution?teacher_id={report_params['teacher_id']}"
           f"&year={report_params['year']}&class_id={report_params['class_id']}"
           f"&student_id={report_params['student_id']}&regua=70.0")
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert "evolution" in response.json
    assert response.json['regua_meta'] == 70.0
    assert isinstance(response.json['evolution'], list)

def test_report_fail_student_without_class(client, report_params):
    # Act: Tenta filtrar por aluno sem informar a turma (Deve falhar)
    url = f"/reports/performance?teacher_id={report_params['teacher_id']}&year={report_params['year']}&student_id={report_params['student_id']}"
    response = client.get(url)

    # Assert
    assert response.status_code == 400
    assert "informe a turma" in response.json['message']

def test_report_missing_required_params(client):
    # Act: Tenta acessar sem parâmetros obrigatórios
    response = client.get("/reports/performance")

    # Assert
    assert response.status_code == 400
    assert "obrigatórios" in response.json['message']

def test_report_student_details_success(client, report_params):
    # Act: Removido o parâmetro year da query string
    url = (f"/reports/student-details?teacher_id={report_params['teacher_id']}"
           f"&class_id={report_params['class_id']}"
           f"&student_id={report_params['student_id']}")
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    # Verifica se a dificuldade está vindo no primeiro registro do primeiro tema
    if response.json:
        first_theme = list(response.json.keys())[0]
        assert "difficulty" in response.json[first_theme][0]
        