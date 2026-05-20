import pytest

from app.services.task_service import (
    complete_task,
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    reset_tasks,
    update_task,
)


@pytest.fixture(autouse=True)
def clear_tasks():
    # Executa antes de cada teste para começar com a lista vazia
    reset_tasks()


def test_create_task():
    task = create_task({"title": "Estudar Pytest"})

    assert task["id"] == 1
    assert task["title"] == "Estudar Pytest"
    assert task["completed"] is False


def test_get_all_tasks_empty():
    assert get_all_tasks() == []


def test_get_all_tasks_with_items():
    create_task({"title": "Tarefa 1"})
    create_task({"title": "Tarefa 2"})

    assert len(get_all_tasks()) == 2


def test_get_task_by_id_found():
    task = create_task({"title": "Buscar tarefa"})

    result = get_task_by_id(task["id"])

    assert result["title"] == "Buscar tarefa"


def test_get_task_by_id_not_found():
    result = get_task_by_id(999)

    assert result is None


def test_update_task():
    task = create_task({"title": "Título antigo"})

    updated = update_task(task["id"], {"title": "Título novo"})

    assert updated["title"] == "Título novo"


def test_update_task_not_found():
    result = update_task(999, {"title": "Não existe"})

    assert result is None


def test_delete_task():
    task = create_task({"title": "Excluir tarefa"})

    result = delete_task(task["id"])

    assert result is True
    assert get_all_tasks() == []


def test_delete_task_not_found():
    result = delete_task(999)

    assert result is False


def test_complete_task():
    task = create_task({"title": "Concluir tarefa"})

    completed = complete_task(task["id"])

    assert completed["completed"] is True


def test_complete_task_not_found():
    result = complete_task(999)

    assert result is None


def test_create_duplicate_task_should_return_none():
    """
    Testa se o sistema impede tarefas duplicadas.
    """

    create_task({"title": "Tarefa repetida"})

    duplicated = create_task({"title": "Tarefa repetida"})

    assert duplicated is None
