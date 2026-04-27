from flask import Blueprint, request, jsonify
from controllers.play import (
    get_student_login_data, get_characters_preview, initialize_game_session, get_initial_questions,
    get_regions_status, get_smart_questions, save_questions_progress, update_challenge_progress
)

play = Blueprint('play', __name__)

@play.route('/play/login', methods=['POST'])
def play_login():
    data = request.get_json()
    res = get_student_login_data(data.get('ra'), data.get('password'))
    return jsonify(res) if res else (jsonify({'message': 'RA ou Senha incorretos'}), 401)

@play.route('/play/characters/preview/<int:id_student>/<int:id_class>', methods=['GET'])
def play_preview(id_student, id_class):
    return jsonify(get_characters_preview(id_student, id_class))

@play.route('/play/select-character', methods=['POST'])
def play_select():
    data = request.get_json()
    game, match = initialize_game_session(data['idStudent'], data['idClass'], data['idCharacter'], data['matchName'])
    if game and match:
        return jsonify({
            'idGame': game.id, 'gold': game.gold, 'idMatch': match.id,
            'scores': {'strength': match.scoreStrength, 'agility': match.scoreAgility, 'resistance': match.scoreResistance, 'wisdom': match.scoreWisdom}
        }), 201
    return jsonify({'message': 'Erro ao iniciar'}), 500

@play.route('/play/regions/status/<int:id_game_match>', methods=['GET'])
def play_regions_status(id_game_match):
    return jsonify(get_regions_status(id_game_match))

@play.route('/play/questions/initial', methods=['GET'])
def play_list_initial_questions():
    # Retorna as 5 questões iniciais pré-definidas
    questions = get_initial_questions()
    
    if questions:
        return jsonify(questions), 200
    
    return jsonify({'message': 'Questões iniciais não localizadas no banco.'}), 404

@play.route('/play/questions/smart/<int:id_student>/<int:id_class>', methods=['GET'])
def play_smart_questions(id_student, id_class):
    id_region = request.args.get('region', type=int)
    return jsonify(get_smart_questions(id_student, id_class, id_region))

@play.route('/play/save-questions', methods=['POST'])
def play_save_questions():
    data = request.get_json()
    step = save_questions_progress(data['idGameMatch'], data['idRegion'], data['answers'])
    
    if step:
        # Adicionamos o , 201 no final da tupla de retorno
        return jsonify({'message': 'Questões salvas', 'idStep': step.id}), 201
    
    return jsonify({'message': 'Erro ao salvar questões'}), 500
    
@play.route('/play/save-challenge', methods=['POST'])
def play_save_challenge():
    data = request.get_json()
    
    # Aqui está o segredo: pegamos o 'number' que você adicionou no teste
    challenge = update_challenge_progress(
        data['idStep'], 
        data['points'], 
        data['number']  # <--- Passando o valor que veio do teste
    )
    
    if challenge:
        return jsonify({'message': 'Sucesso', 'idGamesChallenge': challenge.id}), 200
    
    return jsonify({'message': 'Erro ao salvar desafio'}), 404

