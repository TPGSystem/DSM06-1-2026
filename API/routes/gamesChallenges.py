from flask import Blueprint, request, jsonify
from models.database import db
from controllers.gamesChallenges import *

gamesChallenges = Blueprint('gamesChallenges', __name__)

@gamesChallenges.route('/gamesChallenges', methods=['GET'])
def list_():
    all_recs = get_all()
    return jsonify([{
        'id': rec.id, 
        'idGamesSteps': rec.idGamesSteps, 
        'number': rec.number, 
        'dateTime': rec.dateTime, 
        'points': rec.points
    } for rec in all_recs])

@gamesChallenges.route('/gamesChallenges/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({
            'id': rec.id,  
            'idGamesSteps': rec.idGamesSteps, 
            'number': rec.number, 
            'dateTime': rec.dateTime, 
            'points': rec.points
        })
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesChallenges.route('/gamesChallenges', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'idGamesSteps' not in data or 'number' not in data:
        return jsonify({'error': 'Dados obrigatórios ausentes (idGamesSteps, number)'}), 400

    rec = create(data['idGamesSteps'], 
                 data['number'], 
                 data.get('dateTime'), 
                 data.get('points', 0))

    return jsonify({
        'id': rec.id,  
        'idGamesSteps': rec.idGamesSteps, 
        'number': rec.number, 
        'points': rec.points
    }), 201

@gamesChallenges.route('/gamesChallenges/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()
    
    rec = update(id, 
                 data.get('idGamesSteps'), 
                 data.get('number'), 
                 data.get('dateTime'), 
                 data.get('points'))
    
    if rec:
        return jsonify({
            'id': rec.id,  
            'idGamesSteps': rec.idGamesSteps, 
            'number': rec.number, 
            'points': rec.points
        })
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesChallenges.route('/gamesChallenges/<int:id>', methods=['DELETE'])
def delete_(id):
    if delete(id):
        return jsonify({'message': 'Registro Excluído com Sucesso'})
    return jsonify({'message': 'Registro Não Encontrado'}), 404
