from flask import Blueprint, jsonify
from controllers.components import *

components = Blueprint('components', __name__)

@components.route('/components', methods=['GET'])
def list_():
    return jsonify(get_all())

@components.route('/components/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify(rec)
    return jsonify({'message': 'Registro Não Encontrado'}), 404
