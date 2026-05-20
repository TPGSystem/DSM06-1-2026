import pytest

from app import create_app
from app.services.task_service import reset_tasks


@pytest.fixture
def client():
    reset_tasks()

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_complete_task_flow(client):
    created = client.post("/tasks", json={"title": "Fluxo completo"})
    task_id = created.get_json()["id"]

    fetched = client.get(f"/tasks/{task_id}")

    assert fetched.status_code == 200
    assert fetched.get_json()["title"] == "Fluxo completo"

    updated = client.put(
        f"/tasks/{task_id}",
        json={"title": "Fluxo atualizado"},
    )

    assert updated.status_code == 200
    assert updated.get_json()["title"] == "Fluxo atualizado"

    completed = client.patch(f"/tasks/{task_id}/complete")

    assert completed.status_code == 200
    assert completed.get_json()["completed"] is True

    deleted = client.delete(f"/tasks/{task_id}")

    assert deleted.status_code == 204

    final_check = client.get(f"/tasks/{task_id}")

    assert final_check.status_code == 404


def test_multiple_tasks_flow(client):
    client.post("/tasks", json={"title": "Tarefa A"})
    client.post("/tasks", json={"title": "Tarefa B"})
    client.post("/tasks", json={"title": "Tarefa C"})

    response = client.get("/tasks")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 3


def test_invalid_task_creation(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 400
    assert response.get_json()["error"] == "title is required"
