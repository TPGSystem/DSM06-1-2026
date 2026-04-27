from flask import Blueprint, jsonify
from controllers.characters import get_all, get_by_id

characters = Blueprint('characters', __name__)

@characters.route('/characters', methods=['GET'])
def list_():
    return jsonify(get_all())

@characters.route('/characters/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify(rec)
    return jsonify({'message': 'Registro Não Encontrado'}), 404
