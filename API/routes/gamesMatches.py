from flask import Blueprint, request, jsonify
from models.database import db
from controllers.gamesMatches import *
from sqlalchemy import text

gamesMatches = Blueprint('gamesMatches', __name__)

@gamesMatches.route('/gamesMatches', methods=['GET'])
def list_():
    all_recs = get_all()
    return jsonify([{
        'id': rec.id, 
        'idGame': rec.idGame,
        'idCharacter': rec.idCharacter,
        'name': rec.name,
        'scorePoints': rec.scorePoints,
        'scoreStrength': rec.scoreStrength,
        'scoreAgility': rec.scoreAgility,
        'scoreResistance': rec.scoreResistance,
        'scoreWisdom': rec.scoreWisdom
    } for rec in all_recs])

@gamesMatches.route('/gamesMatches/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({
            'id': rec.id,  
            'idGame': rec.idGame,
            'idCharacter': rec.idCharacter,
            'name': rec.name,
            'scorePoints': rec.scorePoints,
            'scoreStrength': rec.scoreStrength,
            'scoreAgility': rec.scoreAgility,
            'scoreResistance': rec.scoreResistance,
            'scoreWisdom': rec.scoreWisdom
        })
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesMatches.route('/gamesMatches', methods=['POST'])
def create_():
    data = request.get_json()
    # Campos obrigatórios para criação
    required = ['idGame', 'idCharacter', 'name']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Campo {field} ausente'}), 400

    rec = create(data['idGame'], data['idCharacter'], data['name'],
                 data.get('scorePoints', 0), data.get('scoreStrength', 0),
                 data.get('scoreAgility', 0), data.get('scoreResistance', 0),
                 data.get('scoreWisdom', 0))

    return jsonify({'id': rec.id, 'name': rec.name}), 201

@gamesMatches.route('/gamesMatches/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()
    rec = update(id, data.get('idGame'), data.get('idCharacter'), data.get('name'),
                 data.get('scorePoints'), data.get('scoreStrength'),
                 data.get('scoreAgility'), data.get('scoreResistance'),
                 data.get('scoreWisdom'))
    
    if rec:
        return jsonify({'id': rec.id, 'name': rec.name})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesMatches.route('/gamesMatches/<int:id>', methods=['DELETE'])
def delete_(id):
    # Verificação de dependências
    checks = [
        ("GamesQuestions", "idGameMatches"),
        ("GamesChallenges", "idGameMatches"),
        ("GamesSteps", "idGameMatches")
    ]
    
    for table, column in checks:
        used = db.session.execute(
            text(f"SELECT COUNT(*) FROM {table} WHERE {column} = :id"), {'id': id}
        ).scalar()
        if used > 0:
            return jsonify({'message': f'Registro vinculado em {table} e não pode ser excluído.'}), 400

    if delete(id):
        return jsonify({'message': 'Registro Excluído com Sucesso'})
    return jsonify({'message': 'Registro Não Encontrado'}), 404
