from flask import Blueprint, request, jsonify
from models.database import db
from controllers.questions import *
from sqlalchemy import text

questions = Blueprint('questions', __name__)

@questions.route('/questions', methods=['GET'])
def list_():
    return jsonify(get_all())

@questions.route('/questions/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify(rec)
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@questions.route('/questions', methods=['POST'])
def create_():
    data = request.get_json()
    # Validação de campos obrigatórios
    required = ['idQuestionType', 'idTheme', 'question', 'idValidation1', 'idValidation2', 'idValidation3', 'idValidation4']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Campo {field} é obrigatório'}), 400

    # Verifica se os campos picutres estão vazio e converte para binário
    def normalize_picture(val):
        if val in ('', None):
            return None  # ou b''
        return val if isinstance(val, bytes) else val.encode('utf-8')

    for key in ['picture1', 'picture2', 'picture3', 'picture4']:
        data[key] = normalize_picture(data.get(key))

    rec = create(data['idQuestionType'], data.get('idRegion'), data['idTheme'], data['question'],
                 data.get('response1'), data.get('response2'), data.get('response3'), data.get('response4'),
                 data.get('picture1'), data.get('picture2'), data.get('picture3'), data.get('picture4'),
                 data['idValidation1'], data['idValidation2'], data['idValidation3'], data['idValidation4'])

    return jsonify({'id': rec.id, 'question': rec.question}), 201

@questions.route('/questions/<int:id>', methods=['PUT'])
def update_(id):
    data = request.get_json()

    rec = update(id, 
                 data.get('idQuestionType'), data.get('idRegion'), data.get('idTheme'),
                 data.get('question'), data.get('response1'), data.get('response2'),
                 data.get('response3'), data.get('response4'), data.get('picture1'),
                 data.get('picture2'), data.get('picture3'), data.get('picture4'),
                 data.get('idValidation1'), data.get('idValidation2'),
                 data.get('idValidation3'), data.get('idValidation4'))
    
    if rec:
        return jsonify({'id': rec.id, 'question': rec.question})
    return jsonify({'message': 'Registro Não Encontrado'}), 404

@questions.route('/questions/<int:id>', methods=['DELETE'])
def delete_(id):
    used = db.session.execute(
        text("SELECT COUNT(*) FROM QuestionsSkills WHERE idQuestion = :id"), {'id': id}).scalar()
    
    if used > 0:
        return jsonify({'message': 'Esta questão está vinculada a Habilidades e não pode ser excluída.'}), 400

    if delete(id):
        return jsonify({'message': 'Registro Excluído com Sucesso'})
    return jsonify({'message': 'Registro Não Encontrado'}), 404
