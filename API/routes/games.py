from flask import Blueprint, request, jsonify
from models.database import db
from controllers.games import *
from sqlalchemy import text

games = Blueprint('games', __name__)

@games.route('/games', methods=['GET'])
def list_():
    return jsonify(get_all())

@games.route('/games/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify(rec)
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@games.route('/games', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'idStudent' not in data or 'idClass' not in data:
        return jsonify({'error': 'Dados obrigatórios ausentes (idStudent, idClass)'}), 400

    rec = create(data['idStudent'], data['idClass'], data.get('gold', 0))
    return jsonify({
        'id': rec.id, 
        'idStudent': rec.idStudent,
        'idClass': rec.idClass, 
        'gold': rec.gold
    }), 201

@games.route('/games/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()
    
    rec = update(id, data.get('idStudent'), data.get('idClass'), data.get('gold'))
    
    if rec:
        return jsonify({
            'id': rec.id, 
            'idStudent': rec.idStudent,
            'idClass': rec.idClass,
            'gold': rec.gold
        })
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@games.route('/games/<int:id>', methods=['DELETE'])
def delete_(id):
    # Verificação de integridade na tabela GamesMatches
    used = db.session.execute(
        text("SELECT COUNT(*) FROM GamesMatches WHERE idGame = :id"), {'id': id}
    ).scalar()
    
    if used > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na tabela de Partidas e não pode ser excluído.'}), 400

    if delete(id):
        return jsonify({'message': 'Registro Excluído com Sucesso'})
    return jsonify({'message': 'Registro Não Encontrado'}), 404
