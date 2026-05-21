from models.database import db, Students, Characters, Games, GamesMatches, Regions, GamesSteps, Questions, QuestionsSkills, GamesQuestions, GamesChallenges
from sqlalchemy import func, desc
from werkzeug.security import check_password_hash
from datetime import datetime
import random

def get_student_login_data(ra, password):
    rec = Students.query.filter_by(ra=ra).first()
    if rec and check_password_hash(rec.password, password):
        return {
            "authenticated": True,
            "student": {"id": rec.id, "name": rec.name, "ra": rec.ra},
            "class": {
                "id": rec.idClass,
                "schoolYear": rec.classe.schoolYear if rec.classe else None,
                "dsYearSerie": rec.classe.yearSerie.descryption if rec.classe and rec.classe.yearSerie else None,
                "dsComponent": rec.classe.component.descryption if rec.classe and rec.classe.component else None,
                "dsTeacher": rec.classe.teacher.name if rec.classe and rec.classe.teacher else None
            }
        }
    return None

def get_characters_preview(id_student, id_class):
    all_characters = Characters.query.all()
    game_record = Games.query.filter_by(idStudent=id_student, idClass=id_class).first()
    result = []
    for char in all_characters:
        char_data = {
            'id': char.id, 'number': char.number,
            'dsValidation': char.validation.descryption if char.validation else None,
            'scoreStrength': char.scoreStrength, 'scoreAgility': char.scoreAgility,
            'scoreResistance': char.scoreResistance, 'scoreWisdom': char.scoreWisdom,
            'isUsed': False
        }
        if game_record:
            match = GamesMatches.query.filter_by(idGame=game_record.id, idCharacter=char.id).first()
            if match:
                char_data.update({
                    'scoreStrength': match.scoreStrength, 'scoreAgility': match.scoreAgility,
                    'scoreResistance': match.scoreResistance, 'scoreWisdom': match.scoreWisdom,
                    'isUsed': True
                })
        result.append(char_data)
    return result

def initialize_game_session(id_student, id_class, id_character, match_name):
    game_record = Games.query.filter_by(idStudent=id_student, idClass=id_class).first()
    if not game_record:
        game_record = Games(idStudent=id_student, idClass=id_class, gold=0)
        db.session.add(game_record)
        db.session.flush()

    match_record = GamesMatches.query.filter_by(idGame=game_record.id, idCharacter=id_character).first()
    if not match_record:
        char_base = db.session.get(Characters, id_character)
        if not char_base: return None, None
        match_record = GamesMatches(
            idGame=game_record.id, idCharacter=id_character, name=match_name, scorePoints=0,
            scoreStrength=char_base.scoreStrength, scoreAgility=char_base.scoreAgility,
            scoreResistance=char_base.scoreResistance, scoreWisdom=char_base.scoreWisdom
        )
        db.session.add(match_record)
    db.session.commit()
    return game_record, match_record

def get_regions_status(id_game_match):
    all_regions = Regions.query.all()
    result = []
    for region in all_regions:
        last_step = GamesSteps.query.filter_by(idGameMatch=id_game_match, idRegion=region.id).order_by(GamesSteps.id.desc()).first()
        status = -1
        if last_step:
            status = 1 if (last_step.completedQuestions and last_step.completedChallenges) else 0
        result.append({'id': region.id, 'descryption': region.descryption, 'status': status})
    return result

def get_initial_questions():
    # Busca as questões com IDs de 1 a 5
    # Usamos o filtro 'in_' para garantir que pegamos exatamente esse intervalo
    registers = Questions.query.filter(Questions.id.in_([1, 2, 3, 4, 5])).all()
    
    result = []

    for rec in registers:
        responses = [
            {'text': rec.response1, 'idValidation': rec.idValidation1},
            {'text': rec.response2, 'idValidation': rec.idValidation2},
            {'text': rec.response3, 'idValidation': rec.idValidation3},
            {'text': rec.response4, 'idValidation': rec.idValidation4}
        ]

        correct_answer = None

        for resp in responses:
            if resp["idValidation"] == 3:
                correct_answer = resp["text"]
                break

        result.append({
            'id': rec.id,
            'question': rec.question,
            'idTheme': rec.idTheme,
            'dsTheme': rec.theme.descryption if rec.theme else None,
            'idQuestionType': rec.idQuestionType,
            'dsQuestionType': rec.questionType.descryption if rec.questionType else None,
            'responses': responses,
            'correctAnswer': correct_answer
        })

    return result
    
def get_smart_questions(id_student, id_class, id_region=None):
    error_ranking = db.session.query(
        Questions.idTheme, func.count(Questions.idTheme).label('total_errors'),
        func.avg(QuestionsSkills.difficulty).label('avg_diff')
    ).join(GamesQuestions, Questions.id == GamesQuestions.idQuestion)\
     .join(QuestionsSkills, Questions.id == QuestionsSkills.idQuestion)\
     .join(GamesSteps, GamesQuestions.idGamesSteps == GamesSteps.id)\
     .join(GamesMatches, GamesSteps.idGameMatch == GamesMatches.id)\
     .join(Games, GamesMatches.idGame == Games.id)\
     .filter(Games.idStudent == id_student, GamesQuestions.points == 0)\
     .group_by(Questions.idTheme).order_by(desc('total_errors')).all()

    theme_a = error_ranking[0].idTheme if len(error_ranking) > 0 else None
    theme_b = error_ranking[1].idTheme if len(error_ranking) > 1 else None
    
    answered_ids = [r[0] for r in db.session.query(GamesQuestions.idQuestion).join(GamesSteps).join(GamesMatches).join(Games).filter(Games.idStudent == id_student, Games.idClass == id_class).all()]

    final_questions = []

    def fetch_qs(theme_id, limit, exclude):
        query = QuestionsSkills.query.join(Questions).filter(QuestionsSkills.available == True, ~QuestionsSkills.idQuestion.in_(exclude))
        if theme_id: query = query.filter(Questions.idTheme == theme_id)
        if id_region:
            reg_q = query.filter(Questions.idRegion == id_region).limit(limit).all()
            if len(reg_q) >= limit: return reg_q
        return query.limit(limit).all()

    final_questions.extend(fetch_qs(theme_a, 2, answered_ids))
    curr_excl = answered_ids + [q.idQuestion for q in final_questions]
    final_questions.extend(fetch_qs(theme_b, 2, curr_excl))
    
    q5 = QuestionsSkills.query.join(Questions).filter(~Questions.idTheme.in_([theme_a, theme_b] if theme_a else [0]), ~QuestionsSkills.idQuestion.in_(answered_ids + [q.idQuestion for q in final_questions])).order_by(func.rand()).first()
    if q5: final_questions.append(q5)

    return [{
        'id': reg.question.id, 'question': reg.question.question, 'difficulty': reg.difficulty,
        'skill': reg.skill.skill if reg.skill else None,
        'responses': [
            {'text': reg.question.response1, 'validation': reg.question.validation1.descryption if reg.question.validation1 else None},
            {'text': reg.question.response2, 'validation': reg.question.validation2.descryption if reg.question.validation2 else None},
            {'text': reg.question.response3, 'validation': reg.question.validation3.descryption if reg.question.validation3 else None},
            {'text': reg.question.response4, 'validation': reg.question.validation4.descryption if reg.question.validation4 else None}
        ]
    } for reg in final_questions[:5]]

def save_questions_progress(id_game_match, id_region, answers):
    try:
        new_step = GamesSteps(idGameMatch=id_game_match, idRegion=id_region, dateTime=datetime.now(), completedQuestions=True, completedChallenges=False)
        db.session.add(new_step)
        db.session.flush()
        pts_total = 0
        for a in answers:
            db.session.add(GamesQuestions(idGamesSteps=new_step.id, idQuestion=a['idQuestion'], dateTime=datetime.now(), points=a['points']))
            pts_total += a['points']
        match = db.session.get(GamesMatches, id_game_match)
        if match: match.scorePoints += pts_total

        game = db.session.get(Games, match.idGame)

        if game:
            game.gold += pts_total

        db.session.commit()
        return new_step
    except:
        db.session.rollback()
        return None

def update_challenge_progress(id_step, points, number):
    try:
        step = db.session.get(GamesSteps, id_step)
        if not step:
            return None

        new_challenge_record = GamesChallenges(
            idGamesSteps=id_step,
            dateTime=datetime.now(),
            points=points,
            number=number
        )

        db.session.add(new_challenge_record)

        # Marca o desafio/boss como concluído
        step.completedChallenges = True

        # Atualiza pontuação da partida e gold geral do jogo
        match = db.session.get(GamesMatches, step.idGameMatch)

        if match:
            match.scorePoints += points

            game = db.session.get(Games, match.idGame)

            if game:
                game.gold += points

        db.session.commit()
        return new_challenge_record

    except Exception as e:
        db.session.rollback()
        print(f"DEBUG Erro: {str(e)}")
        return None
    