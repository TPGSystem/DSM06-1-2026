import pytest
import pymysql
from app import app as flask_app
from models.database import db
from database.seeds import DataSeeder  # Certifique-se de importar seu Seeder

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    db_name = "TPGSystem_test"
    connection = pymysql.connect(host='localhost', user='root', password='')
##    connection = pymysql.connect(host='localhost', user='root', password='masterkey')
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    finally:
        connection.close()

@pytest.fixture
def client():
    # Força as configurações de teste
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/TPGSystem_test"
##    flask_app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:masterkey@localhost/TPGSystem_test"
    with flask_app.app_context():
        # 1. Cria as tabelas do zero
        db.create_all()
        
        DataSeeder.run()
        
        with flask_app.test_client() as client:
            yield client
            
        db.session.remove()
        db.drop_all()
        