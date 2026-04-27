from models.database import db, GamesChallenges

def get_all():
    return GamesChallenges.query.all()

def get_by_id(id):
    return GamesChallenges.query.get(id)

def create(idGamesSteps, number, dateTime, points):
    new = GamesChallenges(idGamesSteps=idGamesSteps,
                          number=number,
                          dateTime=dateTime,
                          points=points)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, idGamesSteps, number, dateTime, points):
    rec = GamesChallenges.query.get(id)
    if rec:
        # Atualização Parcial
        rec.idGamesSteps = idGamesSteps if idGamesSteps is not None else rec.idGamesSteps
        rec.number = number if number is not None else rec.number
        rec.dateTime = dateTime if dateTime is not None else rec.dateTime
        rec.points = points if points is not None else rec.points
        db.session.commit()
    return rec

def delete(id):
    rec = GamesChallenges.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
        return True
    return False
