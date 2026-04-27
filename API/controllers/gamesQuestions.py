from models.database import db, GamesQuestions

def get_all():
    return GamesQuestions.query.all()

def get_by_id(id):
    return GamesQuestions.query.get(id)

def create(idGamesSteps, idQuestion, dateTime, points):
    new = GamesQuestions(idGamesSteps=idGamesSteps,
                          idQuestion=idQuestion,
                          dateTime=dateTime,
                          points=points)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, idGamesSteps, idQuestion, dateTime, points):
    rec = GamesQuestions.query.get(id)
    if rec:
        rec.idGamesSteps = idGamesSteps if idGamesSteps is not None else rec.idGamesSteps
        rec.idQuestion = idQuestion if idQuestion is not None else rec.idQuestion
        rec.dateTime = dateTime if dateTime is not None else rec.dateTime
        rec.points = points if points is not None else rec.points
        db.session.commit()
    return rec

def delete(id):
    rec = GamesQuestions.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
        return True
    return False
