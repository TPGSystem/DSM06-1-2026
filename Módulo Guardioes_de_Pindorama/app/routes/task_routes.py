"""
Arquivo responsável pelas rotas da API.

Aqui lidamos com:
- requisições HTTP
- respostas JSON
- códigos de status HTTP

A regra de negócio fica no arquivo task_service.py.
"""

from flask import Blueprint, jsonify, request

from app.services.task_service import (
    complete_task,
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
)

# Cria um Blueprint para organizar as rotas de tarefas
task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@task_bp.route("/status", methods=["GET"])
def status():
    """
    Rota simples para verificar se a API está funcionando.
    """
    return jsonify({"status": "ok"}), 200


@task_bp.route("", methods=["GET"])
def list_tasks():
    """
    Lista todas as tarefas cadastradas.
    """
    return jsonify(get_all_tasks()), 200


@task_bp.route("/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """
    Busca uma tarefa específica pelo ID.
    """
    task = get_task_by_id(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200


@task_bp.route("", methods=["POST"])
def create():
    """
    Cria uma nova tarefa.

    Espera receber um JSON no formato:
    {
        "title": "Nome da tarefa"
    }
    """
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    task = create_task(data)

    return jsonify(task), 201


@task_bp.route("/<int:task_id>", methods=["PUT"])
def update(task_id):
    """
    Atualiza o título de uma tarefa existente.
    """
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400

    task = update_task(task_id, data)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200


@task_bp.route("/<int:task_id>", methods=["DELETE"])
def delete(task_id):
    """
    Remove uma tarefa existente.
    """
    deleted = delete_task(task_id)

    if not deleted:
        return jsonify({"error": "Task not found"}), 404

    return "", 204


@task_bp.route("/<int:task_id>/complete", methods=["PATCH"])
def complete(task_id):
    """
    Marca uma tarefa como concluída.
    """
    task = complete_task(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200
