# Importa a função create_app, responsável por criar a aplicação Flask
from app import create_app

# Cria a aplicação Flask
app = create_app()

# Executa a aplicação somente quando este arquivo for chamado diretamente
if __name__ == "__main__":
    app.run(debug=True)
