from flask import Blueprint, request, jsonify
from models.database import db
from controllers.questionsSkills import *

questionsSkills = Blueprint('questionsSkills', __name__)

@questionsSkills.route('/questionsSkills', methods=['GET'])
def list_():
    return jsonify(get_all())

@questionsSkills.route('/questionsSkills/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify(rec) 
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@questionsSkills.route('/questionsSkills', methods=['POST'])
def create_():
    data = request.get_json()
    # Validação simplificada
    required = ['idQuestion', 'idSkill', 'idYearSerie', 'difficulty', 'available']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Campo {field} é obrigatório'}), 400

    rec = create(data['idQuestion'], data['idSkill'], data['idYearSerie'], data['difficulty'], data['available'])

    return jsonify({
        'id': rec.id, 'idQuestion': rec.idQuestion, 'idSkill': rec.idSkill,
        'idYearSerie': rec.idYearSerie, 'difficulty': rec.difficulty, 'available': rec.available
    }), 201

@questionsSkills.route('/questionsSkills/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    rec = update(id, 
                 data.get('idQuestion'), 
                 data.get('idSkill'), 
                 data.get('idYearSerie'), 
                 data.get('difficulty'), 
                 data.get('available'))
    
    if rec:
        return jsonify({
            'id': rec.id, 'idQuestion': rec.idQuestion, 'idSkill': rec.idSkill,
            'idYearSerie': rec.idYearSerie, 'difficulty': rec.difficulty, 'available': rec.available
        })
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@questionsSkills.route('/questionsSkills/<int:id>', methods=['DELETE'])
def delete_(id):
    if delete(id):
        return jsonify({'message': 'Registro Excluído com Sucesso'})
    return jsonify({'message': 'Registro Não Encontrado'}), 404
