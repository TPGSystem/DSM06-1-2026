from flask import Blueprint, request, jsonify
from models.database import db
from controllers.gamesQuestions import *

gamesQuestions = Blueprint('gamesQuestions', __name__)

@gamesQuestions.route('/gamesQuestions', methods=['GET'])
def list_():
    all_recs = get_all()
    return jsonify([{
        'id': rec.id, 
        'idGamesSteps': rec.idGamesSteps, 
        'idQuestion': rec.idQuestion, 
        'dateTime': rec.dateTime, 
        'points': rec.points
    } for rec in all_recs])

@gamesQuestions.route('/gamesQuestions/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify({
            'id': rec.id,  
            'idGamesSteps': rec.idGamesSteps, 
            'idQuestion': rec.idQuestion, 
            'dateTime': rec.dateTime, 
            'points': rec.points
        })
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesQuestions.route('/gamesQuestions', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'idGamesSteps' not in data:
        return jsonify({'error': 'ID do Passo da Partida Inválido'}), 400
    if 'idQuestion' not in data:
        return jsonify({'error': 'Questão Inválida'}), 400

    rec = create(data['idGamesSteps'], 
                 data['idQuestion'], 
                 data.get('dateTime'), 
                 data.get('points', 0))

    return jsonify({
        'id': rec.id,  
        'idGamesSteps': rec.idGamesSteps, 
        'idQuestion': rec.idQuestion, 
        'points': rec.points
    }), 201

@gamesQuestions.route('/gamesQuestions/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()
    
    rec = update(id, 
                 data.get('idGamesSteps'), 
                 data.get('idQuestion'), 
                 data.get('dateTime'), 
                 data.get('points'))
    
    if rec:
        return jsonify({
            'id': rec.id,  
            'idGamesSteps': rec.idGamesSteps, 
            'idQuestion': rec.idQuestion, 
            'points': rec.points
        })
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@gamesQuestions.route('/gamesQuestions/<int:id>', methods=['DELETE'])
def delete_(id):
    if delete(id):
        return jsonify({'message': 'Registro Excluído com Sucesso'})
    return jsonify({'message': 'Registro Não Encontrado'}), 404
