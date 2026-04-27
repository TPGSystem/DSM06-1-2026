from flask import Blueprint, jsonify
from controllers.validations import *

validations = Blueprint('validations', __name__)

@validations.route('/validations', methods=['GET'])
def list_():
    return jsonify(get_all())

@validations.route('/validations/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify(rec)
    return jsonify({'message': 'Registro Não Encontrado'}), 404
