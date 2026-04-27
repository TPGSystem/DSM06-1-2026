from flask import Blueprint, request, jsonify
from models.database import db
from controllers.students import *
from sqlalchemy import text
from werkzeug.security import generate_password_hash

students = Blueprint('students', __name__)

@students.route('/students/login', methods=['POST'])
def login_():
    data = request.get_json()
    ra = data.get('ra')
    password = data.get('password')

    if not ra or not password:
        return jsonify({'error': 'Ra e senha são obrigatórios'}), 400

    rec = authenticate(ra, password)
    if rec:
        return jsonify({
            'message': 'Login realizado com sucesso',
            'id': rec.id,
            'name': rec.name,
            'ra': rec.ra
        }), 200
    return jsonify({'error': 'Credenciais inválidas'}), 401

@students.route('/students', methods=['GET'])
def list_():
    # Retorna a lista de dicionários formatada pelo Controller
    return jsonify(get_all())

@students.route('/students/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify(rec)
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@students.route('/students', methods=['POST'])
def create_():
    data = request.get_json()
    
    # Validações básicas
    required = ['name', 'ra', 'password', 'birth', 'idClass']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Campo {field} inválido'}), 400

    hashed_password = generate_password_hash(data['password']) 

    rec = create(data['name'], 
                 data['ra'], 
                 hashed_password, 
                 data['birth'], 
                 data['idClass'])

    return jsonify({
        'id': rec.id,  
        'name': rec.name,
        'ra': rec.ra,
        'birth': rec.birth.isoformat() if rec.birth else None,
        'idClass': rec.idClass
    }), 201

@students.route('/students/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()
    
    # Se password vier no JSON, gera hash, senão fica None
    password = data.get('password')
    hashed_password = generate_password_hash(password) if password else None

    rec = update(id, 
                 data.get('name'), 
                 data.get('ra'), 
                 hashed_password, 
                 data.get('birth'), 
                 data.get('idClass'))
    
    if rec:
        return jsonify({
            'id': rec.id,  
            'name': rec.name,
            'ra': rec.ra,
            'birth': rec.birth.isoformat() if rec.birth else None,
            'idClass': rec.idClass
        })
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@students.route('/students/<int:id>', methods=['DELETE'])
def delete_(id):
    # Verificação de integridade antes de deletar
    used = db.session.execute(
        text("SELECT COUNT(*) FROM Games WHERE idStudent = :id"), {'id': id}
    ).scalar()
    
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na tabela de Games e não pode ser excluído.'}), 400

    rec = delete(id)
    if rec:
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404 