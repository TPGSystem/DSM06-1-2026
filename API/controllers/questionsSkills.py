from models.database import db, QuestionsSkills

def get_all():
    registers = QuestionsSkills.query.all()
    return [{
        'id': rec.id, 
        'idQuestion': rec.idQuestion,
        'dsQuestion': rec.question.question if rec.question else None,
        'idSkill': rec.idSkill,
        'dsSkill': rec.skill.skill if rec.skill else None,
        'idYearSerie': rec.idYearSerie,
        'dsYearSerie': rec.yearserie.descryption if rec.yearserie else None, # Corrigido para match com relationship
        'difficulty': rec.difficulty, 
        'available': rec.available
    } for rec in registers]

def get_by_id(id):
    rec = QuestionsSkills.query.get(id)
    if rec:
        return {
            'id': rec.id, 
            'idQuestion': rec.idQuestion,
            'dsQuestion': rec.question.question if rec.question else None,
            'idSkill': rec.idSkill,
            'dsSkill': rec.skill.skill if rec.skill else None,
            'idYearSerie': rec.idYearSerie,
            'dsYearSerie': rec.yearserie.descryption if rec.yearserie else None,
            'difficulty': rec.difficulty,
            'available': rec.available
        }
    return None

def create(idQuestion, idSkill, idYearSerie, difficulty, available):
    new = QuestionsSkills(idQuestion=idQuestion,
                          idSkill=idSkill,
                          idYearSerie=idYearSerie,
                          difficulty=difficulty,
                          available=available)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, idQuestion, idSkill, idYearSerie, difficulty, available):
    rec = QuestionsSkills.query.get(id)
    if rec:
        rec.idQuestion = idQuestion if idQuestion is not None else rec.idQuestion
        rec.idSkill = idSkill if idSkill is not None else rec.idSkill
        rec.idYearSerie = idYearSerie if idYearSerie is not None else rec.idYearSerie
        rec.difficulty = difficulty if difficulty is not None else rec.difficulty
        rec.available = available if available is not None else rec.available
        db.session.commit()
    return rec

def delete(id):
    rec = QuestionsSkills.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
