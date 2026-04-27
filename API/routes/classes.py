from flask import Blueprint, request, jsonify
from models.database import db
from controllers.classes import *
from sqlalchemy import text

classes = Blueprint('classes', __name__)

@classes.route('/classes', methods=['GET'])
def list_():
    return jsonify(get_all())

@classes.route('/classes/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify(rec)
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@classes.route('/classes', methods=['POST'])
def create_():
    data = request.get_json()
    campos = ['schoolYear', 'idYearSerie', 'idComponent', 'idTeacher']
    for campo in campos:
        if campo not in data:
            return jsonify({'error': f'Campo {campo} é obrigatório'}), 400

    rec = create(data['schoolYear'], 
                  data['idYearSerie'], 
                  data['idComponent'], 
                  data['idTeacher'])

    return jsonify({
        'id': rec.id,  
        'schoolYear': rec.schoolYear,
        'idYearSerie': rec.idYearSerie,
        'idComponent': rec.idComponent,
        'idTeacher': rec.IdTeacher # Acessando IdTeacher do Model corretamente
    }), 201

@classes.route('/classes/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()
    
    rec = update(id, 
                  data.get('schoolYear'), 
                  data.get('idYearSerie'), 
                  data.get('idComponent'), 
                  data.get('idTeacher'))
    
    if rec:
        return jsonify({
            'id': rec.id,  
            'schoolYear': rec.schoolYear,
            'idYearSerie': rec.idYearSerie,
            'idComponent': rec.idComponent,
            'idTeacher': rec.IdTeacher
        })
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@classes.route('/classes/<int:id>', methods=['DELETE'])
def delete_(id):
    used_student = db.session.execute(text("SELECT COUNT(*) FROM Students WHERE idClass = :id"), {'id': id}).scalar()
    if used_student > 0:
        return jsonify({'message': 'Este registro está sendo utilizado no Cadastro de Estudantes.'}), 400

    used_games = db.session.execute(text("SELECT COUNT(*) FROM Games WHERE idClass = :id"), {'id': id}).scalar()
    if used_games > 0:
        return jsonify({'message': 'Este registro está sendo utilizado na tabela de Games.'}), 400

    if delete(id):
        return jsonify({'message': 'Registro Excluído com Sucesso'})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@classes.route('/classes/teacher/<int:id_teacher>', methods=['GET'])
def list_by_teacher(id_teacher):
    return jsonify(get_by_teacher(id_teacher))
