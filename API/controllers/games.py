from models.database import db, Games

def get_all():
    registers = Games.query.all()
    return [{
        'id': rec.id, 
        'idStudent': rec.idStudent,
        'nmStudent': rec.student.nmStudent if rec.student else None,
        'idClass': rec.idClass,
        'dsClass': rec.classe.descryption if rec.classe else None,
        'gold': rec.gold
    } for rec in registers]

def get_by_id(id):
    rec = Games.query.get(id)
    if rec:
        return {
            'id': rec.id, 
            'idStudent': rec.idStudent,
            'nmStudent': rec.student.nmStudent if rec.student else None,
            'idClass': rec.idClass,
            'dsClass': rec.classe.descryption if rec.classe else None,
            'gold': rec.gold
        }
    return None

def create(idStudent, idClass, gold):
    new = Games(idStudent=idStudent, idClass=idClass, gold=gold)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, idStudent, idClass, gold):
    rec = Games.query.get(id)
    if rec:
        rec.idStudent = idStudent if idStudent is not None else rec.idStudent
        rec.idClass = idClass if idClass is not None else rec.idClass
        rec.gold = gold if gold is not None else rec.gold
        db.session.commit()
    return rec

def delete(id):
    rec = Games.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
        return True
    return False