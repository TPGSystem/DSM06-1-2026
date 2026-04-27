from models.database import db, Skills

def get_all():
    registers = Skills.query.all()
    return [{
        'id': rec.id, 
        'idComponent': rec.idComponent,
        'dsComponent': rec.component.descryption if rec.component else None,
        'skill': rec.skill,
        'comment': rec.comment,
        'skillCodeCP': rec.skillCodeCP,
        'skillCodeBNCC': rec.skillCodeBNCC # Ajustado para bater com o Model
    } for rec in registers]

def get_by_id(id):
    rec = Skills.query.get(id)
    if rec:
        return {
            'id': rec.id, 
            'idComponent': rec.idComponent,
            'dsComponent': rec.component.descryption if rec.component else None,
            'skill': rec.skill,
            'comment': rec.comment,
            'skillCodeCP': rec.skillCodeCP,
            'skillCodeBNCC': rec.skillCodeBNCC
        }
    return None

def create(idComponent, skill, comment, skillCodeCP, skillCodeBNCC):
    new = Skills(idComponent=idComponent,
                 skill=skill,
                 comment=comment,
                 skillCodeCP=skillCodeCP,
                 skillCodeBNCC=skillCodeBNCC)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, idComponent, skill, comment, skillCodeCP, skillCodeBNCC):
    rec = Skills.query.get(id)
    if rec:
        rec.idComponent = idComponent if idComponent is not None else rec.idComponent
        rec.skill = skill if skill is not None else rec.skill
        rec.comment = comment if comment is not None else rec.comment
        rec.skillCodeCP = skillCodeCP if skillCodeCP is not None else rec.skillCodeCP
        rec.skillCodeBNCC = skillCodeBNCC if skillCodeBNCC is not None else rec.skillCodeBNCC
        db.session.commit()
    return rec

def delete(id):
    rec = Skills.query.get(id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec
