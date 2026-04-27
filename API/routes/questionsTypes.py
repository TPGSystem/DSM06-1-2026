from flask import Blueprint, jsonify
from controllers.questionsTypes import *

questionsTypes = Blueprint('questionsTypes', __name__)

@questionsTypes.route('/questionstypes', methods=['GET'])
def list_():
    return jsonify(get_all())

@questionsTypes.route('/questionstypes/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify(rec)
    return jsonify({'message': 'Registro Não Encontrado'}), 404
