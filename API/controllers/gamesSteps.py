from models.database import db, GamesSteps

def get_all():
    return GamesSteps.query.all()

def get_by_id(id):
    return GamesSteps.query.get(id)

def create(idGameMatch, idRegion, dateTime, completedQuestions, completedChallenges):
    new = GamesSteps(idGameMatch=idGameMatch,
                     idRegion=idRegion,
                     dateTime=dateTime,
                     completedQuestions=completedQuestions,
                     completedChallenges=completedChallenges)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, idGameMatch, idRegion, dateTime, completedQuestions, completedChallenges):
    rec = GamesSteps.query.get(id)
    if rec:
        # Atualização Parcial
        rec.idGameMatch = idGameMatch if idGameMatch is not None else rec.idGameMatch
        rec.idRegion = idRegion if idRegion is not None else rec.idRegion
        rec.dateTime = dateTime if dateTime is not None else rec.dateTime
        rec.completedQuestions = completedQuestions if completedQuestions is not None else rec.completedQuestions
        rec.completedChallenges = completedChallenges if completedChallenges is not None else rec.completedChallenges
        db.session.commit()
    return rec

def delete(id):
    rec = GamesSteps.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
        return True
    return False
