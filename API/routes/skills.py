from flask import Blueprint, request, jsonify
from models.database import db
from controllers.skills import *
from sqlalchemy import text

skills = Blueprint('skills', __name__)

@skills.route('/skills', methods=['GET'])
def list_():
    return jsonify(get_all())

@skills.route('/skills/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify(rec) 
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@skills.route('/skills', methods=['POST'])
def create_():
    data = request.get_json()
    if not data or 'idComponent' not in data or 'skill' not in data:
        return jsonify({'error': 'Dados obrigatórios ausentes (idComponent, skill)'}), 400

    rec = create(data['idComponent'], 
                 data['skill'], 
                 data.get('comment'), 
                 data.get('skillCodeCP'), 
                 data.get('skillCodeBNCC'))

    return jsonify({
        'id': rec.id,  
        'idComponent': rec.idComponent, 
        'skill': rec.skill, 
        'skillCodeBNCC': rec.skillCodeBNCC
    }), 201

@skills.route('/skills/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    rec = update(id, 
                 data.get('idComponent'), 
                 data.get('skill'), 
                 data.get('comment'), 
                 data.get('skillCodeCP'), 
                 data.get('skillCodeBNCC'))
    
    if rec:
        return jsonify({
            'id': rec.id,  
            'idComponent': rec.idComponent, 
            'skill': rec.skill, 
            'skillCodeBNCC': rec.skillCodeBNCC
        })
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@skills.route('/skills/<int:id>', methods=['DELETE'])
def delete_(id):
    # Verificação de integridade na tabela associativa QuestionsSkills
    used = db.session.execute(
        text("SELECT COUNT(*) FROM QuestionsSkills WHERE idSkill = :id"), {'id': id}
    ).scalar()
    
    if used > 0:
        return jsonify({'message': 'Esta habilidade está vinculada a questões e não pode ser excluída.'}), 400

    if delete(id):
        return jsonify({'message': 'Registro Excluído com Sucesso'})

    return jsonify({'message': 'Registro Não Encontrado'}), 404
