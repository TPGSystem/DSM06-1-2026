from flask import Blueprint, jsonify, request
from controllers.reports import get_performance_by_theme, get_engagement_report, get_top_error_questions, get_monthly_evolution, get_student_detailed_answers

reports = Blueprint('reports', __name__)

@reports.route('/reports/performance', methods=['GET'])
def performance_by_theme():
    t_id, year = request.args.get('teacher_id', type=int), request.args.get('year', type=int)
    c_id, s_id = request.args.get('class_id', type=int), request.args.get('student_id', type=int)

    if not t_id or not year: return jsonify({'message': 'Teacher ID e Year são obrigatórios.'}), 400
    if s_id and not c_id: return jsonify({'message': 'Para filtrar por aluno, informe a turma.'}), 400

    return jsonify(get_performance_by_theme(t_id, year, c_id, s_id)), 200

@reports.route('/reports/engagement', methods=['GET'])
def engagement_report():
    t_id, year = request.args.get('teacher_id', type=int), request.args.get('year', type=int)
    if not t_id or not year: return jsonify({'message': 'Teacher ID e Year são obrigatórios.'}), 400
    return jsonify(get_engagement_report(t_id, year)), 200

@reports.route('/reports/top-errors', methods=['GET'])
def top_error_questions():
    t_id, year = request.args.get('teacher_id', type=int), request.args.get('year', type=int)
    c_id, s_id = request.args.get('class_id', type=int), request.args.get('student_id', type=int)

    if not t_id or not year: return jsonify({'message': 'Teacher ID e Year são obrigatórios.'}), 400
    if s_id and not c_id: return jsonify({'message': 'Para filtrar por aluno, informe a turma.'}), 400

    return jsonify(get_top_error_questions(t_id, year, c_id, s_id)), 200

@reports.route('/reports/evolution', methods=['GET'])
def monthly_evolution():
    t_id, year = request.args.get('teacher_id', type=int), request.args.get('year', type=int)
    c_id, s_id = request.args.get('class_id', type=int), request.args.get('student_id', type=int)
    th_id, regua = request.args.get('theme_id', type=int), request.args.get('regua', type=float, default=75.0)

    if not t_id or not year: return jsonify({'message': 'Teacher ID e Year são obrigatórios.'}), 400
    if s_id and not c_id: return jsonify({'message': 'Para filtrar por aluno, informe a turma.'}), 400

    data = get_monthly_evolution(t_id, year, c_id, s_id, th_id)
    return jsonify({'evolution': data, 'regua_meta': regua}), 200

@reports.route('/reports/student-details', methods=['GET'])
def student_detailed_answers():
    t_id = request.args.get('teacher_id', type=int)
    c_id = request.args.get('class_id', type=int)
    s_id = request.args.get('student_id', type=int)
    th_id = request.args.get('theme_id', type=int)

    # Ano removido, apenas Teacher, Class e Student são essenciais
    if not all([t_id, c_id, s_id]):
        return jsonify({'message': 'Teacher ID, Class ID e Student ID são obrigatórios.'}), 400

    try:
        data = get_student_detailed_answers(t_id, c_id, s_id, th_id)
        return jsonify(data), 200

    except Exception as e:
        return jsonify({'message': 'Erro ao gerar detalhamento do aluno', 'error': str(e)}), 500
    