from models.database import db, Classes

def get_all():
    registers = Classes.query.all()
    return [{
        'id': rec.id, 
        'schoolYear': rec.schoolYear,
        'idYearSerie': rec.idYearSerie,
        'dsYearSerie': rec.yearSerie.descryption if rec.yearSerie else None,
        'idComponent': rec.idComponent,
        'dsComponent': rec.component.descryption if rec.component else None,
        'idTeacher': rec.IdTeacher, # Padronizado para retornar como idTeacher no JSON
        'dsTeacher': rec.teacher.name if rec.teacher else None
    } for rec in registers]

def get_by_id(id):
    # Uso do db.session.get (Padrão SQLAlchemy 2.0)
    rec = db.session.get(Classes, id)
    if rec:
        return {
            'id': rec.id, 
            'schoolYear': rec.schoolYear,
            'idYearSerie': rec.idYearSerie,
            'dsYearSerie': rec.yearSerie.descryption if rec.yearSerie else None,
            'idComponent': rec.idComponent,
            'dsComponent': rec.component.descryption if rec.component else None,
            'idTeacher': rec.IdTeacher,
            'dsTeacher': rec.teacher.name if rec.teacher else None
        }
    return None

def create(schoolYear, idYearSerie, idComponent, idTeacher):
    # O Model espera IdTeacher (com I maiúsculo), mas o argumento da função é idTeacher
    new = Classes(schoolYear=schoolYear,
                  idYearSerie=idYearSerie,
                  idComponent=idComponent,
                  IdTeacher=idTeacher)
    db.session.add(new)
    db.session.commit()
    return new

def update(id, schoolYear, idYearSerie, idComponent, idTeacher):
    rec = db.session.get(Classes, id)
    if rec:
        rec.schoolYear = schoolYear if schoolYear is not None else rec.schoolYear
        rec.idYearSerie = idYearSerie if idYearSerie is not None else rec.idYearSerie
        rec.idComponent = idComponent if idComponent is not None else rec.idComponent
        rec.IdTeacher = idTeacher if idTeacher is not None else rec.IdTeacher
        db.session.commit()
    return rec

def delete(id):
    rec = db.session.get(Classes, id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
        return True
    return False

def get_by_teacher(id_teacher):
    registers = Classes.query.filter_by(IdTeacher=id_teacher).all()
    return [{
        'id': rec.id, 
        'schoolYear': rec.schoolYear,
        'idYearSerie': rec.idYearSerie,
        'dsYearSerie': rec.yearSerie.descryption if rec.yearSerie else None,
        'idComponent': rec.idComponent,
        'dsComponent': rec.component.descryption if rec.component else None,
        'idTeacher': rec.IdTeacher,
        'dsTeacher': rec.teacher.name if rec.teacher else None
    } for rec in registers]
    