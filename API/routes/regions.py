from flask import Blueprint, jsonify
from controllers.regions import *

regions = Blueprint('regions', __name__)

@regions.route('/regions', methods=['GET'])
def list_():
    return jsonify(get_all())

@regions.route('/regions/<int:id>', methods=['GET'])
def get_(id):
    rec = get_by_id(id)
    if rec:
        return jsonify(rec)
    return jsonify({'message': 'Registro Não Encontrado'}), 404
