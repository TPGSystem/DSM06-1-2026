import pytest

from app import create_app
from app.services.task_service import reset_tasks


@pytest.fixture
def client():
    # Reinicia a lista de tarefas antes de cada teste
    reset_tasks()

    # Cria a aplicação Flask em modo de teste
    app = create_app()
    app.config["TESTING"] = True

    # Retorna o cliente de testes do Flask
    with app.test_client() as client:
        yield client


def test_status_route(client):
    response = client.get("/tasks/status")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_task_route(client):
    response = client.post("/tasks", json={"title": "Tarefa de integração"})

    assert response.status_code == 201
    assert response.get_json()["title"] == "Tarefa de integração"


def test_list_tasks_route(client):
    client.post("/tasks", json={"title": "Tarefa 1"})
    client.post("/tasks", json={"title": "Tarefa 2"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_get_task_by_id_route(client):
    created = client.post("/tasks", json={"title": "Buscar por ID"})
    task_id = created.get_json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.get_json()["title"] == "Buscar por ID"


def test_delete_task_route(client):
    created = client.post("/tasks", json={"title": "Excluir integração"})
    task_id = created.get_json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
