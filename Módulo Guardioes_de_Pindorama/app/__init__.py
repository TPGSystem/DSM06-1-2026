# Importa o Flask e o render_template
# Flask cria a aplicação
# render_template permite carregar páginas HTML da pasta templates
from flask import Flask, render_template


def create_app():
    """
    Função responsável por criar e configurar a aplicação Flask.

    Essa estrutura facilita os testes, pois permite criar a aplicação
    dentro dos arquivos de teste sem precisar executar o servidor manualmente.
    """

    # Cria a aplicação Flask
    app = Flask(__name__)

    # Importa o blueprint das rotas de tarefas
    from app.routes.task_routes import task_bp

    # Registra as rotas da API no Flask
    app.register_blueprint(task_bp)

    # Rota principal da interface web
    # Essa tela será usada depois nos testes E2E com Selenium
    @app.route("/")
    def index():
        return render_template("tasks.html")

    # Retorna a aplicação configurada
    return app
