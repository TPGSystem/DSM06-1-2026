from sqlalchemy import func, case, distinct
from models.database import db, GamesQuestions, GamesSteps, GamesMatches, Games, \
                            Questions, Themes, Students, Classes, QuestionsSkills

def get_performance_by_theme(id_teacher, year, id_class=None, id_student=None):
    """Retorna a performance por tema e o resumo geral esperado pelo teste."""
    query = db.session.query(
        Themes.descryption.label('theme'),
        func.count(GamesQuestions.id).label('total'),
        func.sum(case((GamesQuestions.points > 0, 1), else_=0)).label('hits'),
        func.sum(case((GamesQuestions.points == 0, 1), else_=0)).label('misses')
    ).join(Questions, GamesQuestions.idQuestion == Questions.id) \
     .join(Themes, Questions.idTheme == Themes.id) \
     .join(GamesSteps, GamesQuestions.idGamesSteps == GamesSteps.id) \
     .join(GamesMatches, GamesSteps.idGameMatch == GamesMatches.id) \
     .join(Games, GamesMatches.idGame == Games.id) \
     .join(Students, Games.idStudent == Students.id) \
     .join(Classes, Games.idClass == Classes.id)

    query = query.filter(Classes.IdTeacher == id_teacher)
    query = query.filter(Classes.schoolYear == year)

    if id_class:
        query = query.filter(Classes.id == id_class)
    if id_student:
        query = query.filter(Students.id == id_student)

    results = query.group_by(Themes.descryption).all()

    by_theme = []
    total_hits = 0
    total_misses = 0

    for r in results:
        hits = int(r.hits or 0)
        misses = int(r.misses or 0)
        total_hits += hits
        total_misses += misses
        
        by_theme.append({
            "theme": r.theme,
            "total": int(r.total),
            "hits": hits,
            "misses": misses,
            "accuracy_rate": round((hits / r.total) * 100, 2) if r.total > 0 else 0
        })

    # Adicionando a chave 'general_summary' que o teste exige
    return {
        "by_theme": by_theme,
        "general_summary": {
            "hits": total_hits,
            "misses": total_misses,
            "total": total_hits + total_misses
        }
    }

def get_engagement_report(id_teacher, year):
    """Retorna o engajamento de alunos ativos/inativos."""
    students_query = db.session.query(
        Students.id, 
        Students.name,
        Classes.id.label('class_id')
    ).join(Classes, Students.idClass == Classes.id) \
     .filter(Classes.IdTeacher == id_teacher) \
     .filter(Classes.schoolYear == year).all()

    played_ids_query = db.session.query(distinct(Games.idStudent)).all()
    played_ids = [r[0] for r in played_ids_query]

    played = []
    not_played = []

    for s in students_query:
        student_data = {"id": s.id, "name": s.name, "class_id": s.class_id}
        if s.id in played_ids:
            played.append(student_data)
        else:
            not_played.append(student_data)

    return {
        "totals": {
            "total_students": len(students_query),
            "total_played": len(played),
            "total_not_played": len(not_played)
        },
        "details": {
            "played": played,
            "not_played": not_played
        },
        "summary_by_class": []
    }

def get_top_error_questions(id_teacher, year, id_class=None, id_student=None):
    """Identifica questões críticas."""
    query = db.session.query(
        Questions.id,
        Questions.question.label('text'),
        Themes.descryption.label('theme'),
        func.count(GamesQuestions.id).label('error_count'),
        QuestionsSkills.difficulty.label('difficulty')
    ).join(GamesQuestions, Questions.id == GamesQuestions.idQuestion) \
     .join(Themes, Questions.idTheme == Themes.id) \
     .join(GamesSteps, GamesQuestions.idGamesSteps == GamesSteps.id) \
     .join(GamesMatches, GamesSteps.idGameMatch == GamesMatches.id) \
     .join(Games, GamesMatches.idGame == Games.id) \
     .join(Classes, Games.idClass == Classes.id) \
     .join(QuestionsSkills, (QuestionsSkills.idQuestion == Questions.id) & 
                            (QuestionsSkills.idYearSerie == Classes.idYearSerie))

    query = query.filter(Classes.IdTeacher == id_teacher)
    query = query.filter(Classes.schoolYear == year)
    query = query.filter(GamesQuestions.points == 0)

    if id_class:
        query = query.filter(Classes.id == id_class)
    if id_student:
        query = query.filter(Games.idStudent == id_student)

    results = query.group_by(Questions.id, QuestionsSkills.difficulty, Themes.descryption) \
                   .order_by(func.count(GamesQuestions.id).desc()).limit(10).all()

    return [
        {
            "id": r.id,
            "question_text": r.text,
            "theme": r.theme,
            "total_errors": r.error_count,
            "difficulty": r.difficulty
        } for r in results
    ]

def get_monthly_evolution(id_teacher, year, id_class=None, id_student=None, id_theme=None):
    """Retorna apenas a lista de evolução para a rota formatar conforme o teste."""
    query = db.session.query(
        func.month(GamesQuestions.dateTime).label('month'),
        func.count(GamesQuestions.id).label('total'),
        func.sum(case((GamesQuestions.points > 0, 1), else_=0)).label('hits')
    ).join(Questions, GamesQuestions.idQuestion == Questions.id) \
     .join(GamesSteps, GamesQuestions.idGamesSteps == GamesSteps.id) \
     .join(GamesMatches, GamesSteps.idGameMatch == GamesMatches.id) \
     .join(Games, GamesMatches.idGame == Games.id) \
     .join(Students, Games.idStudent == Students.id) \
     .join(Classes, Games.idClass == Classes.id)

    query = query.filter(Classes.IdTeacher == id_teacher)
    query = query.filter(Classes.schoolYear == year)

    if id_class:
        query = query.filter(Classes.id == id_class)
    if id_student:
        query = query.filter(Students.id == id_student)
    if id_theme:
        query = query.filter(Questions.idTheme == id_theme)

    results = query.group_by(func.month(GamesQuestions.dateTime)).order_by('month').all()

    return [
        {
            "month": int(r.month),
            "total": int(r.total),
            "hits": int(r.hits or 0),
            "percentage": round((r.hits / r.total) * 100, 2) if r.total > 0 else 0
        } for r in results
    ]

def get_student_detailed_answers(id_teacher, id_class, id_student, id_theme=None):
    """Relatório detalhado por aluno."""
    query = db.session.query(
        Themes.descryption.label('theme'),
        GamesQuestions.dateTime.label('date'),
        Questions.question.label('question_text'),
        Questions.response1.label('correct_answer'),
        GamesQuestions.points.label('points'),
        QuestionsSkills.difficulty.label('difficulty')
    ).join(Questions, GamesQuestions.idQuestion == Questions.id) \
     .join(Themes, Questions.idTheme == Themes.id) \
     .join(GamesSteps, GamesQuestions.idGamesSteps == GamesSteps.id) \
     .join(GamesMatches, GamesSteps.idGameMatch == GamesMatches.id) \
     .join(Games, GamesMatches.idGame == Games.id) \
     .join(Students, Games.idStudent == Students.id) \
     .join(Classes, Games.idClass == Classes.id) \
     .join(QuestionsSkills, (QuestionsSkills.idQuestion == Questions.id) & 
                            (QuestionsSkills.idYearSerie == Classes.idYearSerie))

    query = query.filter(Classes.IdTeacher == id_teacher)
    query = query.filter(Classes.id == id_class)
    query = query.filter(Students.id == id_student)

    if id_theme:
        query = query.filter(Themes.id == id_theme)

    results = query.order_by(Themes.descryption, GamesQuestions.dateTime.desc()).all()

    grouped = {}
    for r in results:
        if r.theme not in grouped:
            grouped[r.theme] = []
        grouped[r.theme].append({
            "date": r.date.strftime('%d/%m/%Y %H:%M'),
            "question": r.question_text,
            "difficulty": r.difficulty,
            "is_correct": r.points > 0,
            "correct_answer": r.correct_answer
        })
    return grouped
