from flask import Blueprint, request, jsonify
from models.database import db
from controllers.gamesSteps import *
from sqlalchemy import text

gamesSteps = Blueprint('gamesSteps', __name__)

@gamesSteps.route('/gamesSteps', methods=['GET'])
def list_():
    all_recs = get_all()
    return jsonify([{
        'id': rec.id, 
        'idGameMatch': rec.idGameMatch, 
        'idRegion': rec.idRegion, 
        'dateTime': rec.dateTime, 
        'completedQuestions': rec.completedQuestions,
        'completedChallenges': rec.completedChallenges
    } for rec in all_recs])

@gamesSteps.route('/gamesSteps/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({
            'id': rec.id,  
            'idGameMatch': rec.idGameMatch, 
            'idRegion': rec.idRegion, 
            'dateTime': rec.dateTime, 
            'completedQuestions': rec.completedQuestions,
            'completedChallenges': rec.completedChallenges
        })
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesSteps.route('/gamesSteps', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'idGameMatch' not in data or 'idRegion' not in data:
        return jsonify({'error': 'Dados obrigatórios ausentes (idGameMatch, idRegion)'}), 400

    rec = create(data['idGameMatch'], 
                 data['idRegion'], 
                 data.get('dateTime'), 
                 data.get('completedQuestions', False),
                 data.get('completedChallenges', False))

    return jsonify({
        'id': rec.id,  
        'idGameMatch': rec.idGameMatch, 
        'completedQuestions': rec.completedQuestions
    }), 201

@gamesSteps.route('/gamesSteps/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()
    
    rec = update(id, 
                 data.get('idGameMatch'), 
                 data.get('idRegion'), 
                 data.get('dateTime'), 
                 data.get('completedQuestions'),
                 data.get('completedChallenges'))
    
    if rec:
        return jsonify({
            'id': rec.id,  
            'idGameMatch': rec.idGameMatch, 
            'completedQuestions': rec.completedQuestions,
            'completedChallenges': rec.completedChallenges
        })
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesSteps.route('/gamesSteps/<int:id>', methods=['DELETE'])
def delete_(id):
    # Verificação de dependência em GamesQuestions e GamesChallenges
    for table in ["GamesQuestions", "GamesChallenges"]:
        used = db.session.execute(
            text(f"SELECT COUNT(*) FROM {table} WHERE idGamesSteps = :id"), {'id': id}
        ).scalar()
        if used > 0:
            return jsonify({'message': f'Este passo possui registros em {table} e não pode ser excluído.'}), 400

    if delete(id):
        return jsonify({'message': 'Registro Excluído com Sucesso'})
    return jsonify({'message': 'Registro Não Encontrado'}), 404
