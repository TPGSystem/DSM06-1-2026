from models.database import db, GamesMatches

def get_all():
    return GamesMatches.query.all()

def get_by_id(id):
    return GamesMatches.query.get(id)

def create(idGame, idCharacter, name, scorePoints, scoreStrength, scoreAgility, scoreResistance, scoreWisdom):
    new = GamesMatches(idGame=idGame, idCharacter=idCharacter, name=name, 
                       scorePoints=scorePoints, scoreStrength=scoreStrength, 
                       scoreAgility=scoreAgility, scoreResistance=scoreResistance, 
                       scoreWisdom=scoreWisdom)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, idGame, idCharacter, name, scorePoints, scoreStrength, scoreAgility, scoreResistance, scoreWisdom):
    rec = GamesMatches.query.get(id)
    if rec:
        rec.idGame = idGame if idGame is not None else rec.idGame
        rec.idCharacter = idCharacter if idCharacter is not None else rec.idCharacter
        rec.name = name if name is not None else rec.name
        rec.scorePoints = scorePoints if scorePoints is not None else rec.scorePoints
        rec.scoreStrength = scoreStrength if scoreStrength is not None else rec.scoreStrength
        rec.scoreAgility = scoreAgility if scoreAgility is not None else rec.scoreAgility
        rec.scoreResistance = scoreResistance if scoreResistance is not None else rec.scoreResistance
        rec.scoreWisdom = scoreWisdom if scoreWisdom is not None else rec.scoreWisdom
        db.session.commit()
    return rec

def delete(id):
    rec = GamesMatches.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
        return True
    return False
