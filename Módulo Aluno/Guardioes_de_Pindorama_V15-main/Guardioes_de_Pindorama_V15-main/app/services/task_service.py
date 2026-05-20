"""
Arquivo responsável pelas regras de negócio das tarefas.

Aqui não trabalhamos diretamente com HTTP.
Este arquivo apenas cuida da lógica:
- criar tarefa
- listar tarefas
- buscar por ID
- atualizar
- excluir
- concluir tarefa

Neste primeiro momento, usaremos uma lista em memória como "banco de dados".
"""

# Lista que simula o banco de dados
tasks = []

# Variável para controlar o ID automático das tarefas
current_id = 1


def reset_tasks():
    """
    Reinicia o banco em memória.

    Essa função será muito útil nos testes, pois garante que cada teste
    comece com a lista de tarefas vazia.
    """
    global current_id

    tasks.clear()
    current_id = 1


def get_all_tasks():
    """
    Retorna todas as tarefas cadastradas.
    """
    return tasks


def get_task_by_id(task_id):
    """
    Busca uma tarefa pelo ID.

    Se encontrar, retorna a tarefa.
    Se não encontrar, retorna None.
    """
    return next((task for task in tasks if task["id"] == task_id), None)


def create_task(data):
    """
    Cria uma nova tarefa.

    Antes de criar, verifica se já existe uma tarefa com o mesmo título.
    Se existir, retorna None para impedir duplicidade.
    """
    global current_id

    for task in tasks:
        if task["title"].lower() == data["title"].lower():
            return None

    task = {
        "id": current_id,
        "title": data["title"],
        "completed": False,
    }

    tasks.append(task)
    current_id += 1

    return task


def update_task(task_id, data):
    """
    Atualiza o título de uma tarefa existente.

    Se a tarefa não existir, retorna None.
    """
    task = get_task_by_id(task_id)

    if not task:
        return None

    task["title"] = data["title"]

    return task


def delete_task(task_id):
    """
    Remove uma tarefa pelo ID.

    Se a tarefa existir, remove e retorna True.
    Se não existir, retorna False.
    """
    task = get_task_by_id(task_id)

    if not task:
        return False

    tasks.remove(task)

    return True


def complete_task(task_id):
    """
    Marca uma tarefa como concluída.

    Se a tarefa não existir, retorna None.
    """
    task = get_task_by_id(task_id)

    if not task:
        return None

    task["completed"] = True

    return task
