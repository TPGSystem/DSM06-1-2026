from models.database import db, Students
from werkzeug.security import check_password_hash

def authenticate(ra, password):
    # Busca o registro pelo RA
    rec = Students.query.filter_by(ra=ra).first()
    # Verifica se existe e se a senha (hash) bate
    if rec and check_password_hash(rec.password, password):
        return rec    
    return None

def get_all():
    # Busca todos os alunos
    registers = Students.query.all()
    
    students = []
    for rec in registers:
        students.append({
            'id': rec.id,
            'name': rec.name,
            'ra': rec.ra,
            'birth': rec.birth.isoformat() if rec.birth else None,
            'idClass': rec.idClass,
            # Navegação via relacionamento: Student -> Classes -> YearsSeries
            'dsYearSerie': rec.classe.yearSerie.descryption if rec.classe and rec.classe.yearSerie else None
        })
    
    return students
        
def get_by_id(id):
    # rec = Students.query.get(id)
    rec = db.session.get(Students, id)
    
    if rec:
        return {
            'id': rec.id,
            'name': rec.name,
            'ra': rec.ra,
            'birth': rec.birth.isoformat() if rec.birth else None,
            'idClass': rec.idClass,
            'dsYearSerie': rec.classe.yearSerie.descryption if rec.classe and rec.classe.yearSerie else None
        }
    return None

def create(name, ra, password, birth, idClass):
    rec = Students(name = name,
                   ra = ra,
                   password = password,
                   birth = birth,
                   idClass = idClass)
    db.session.add(rec)
    db.session.commit()
    return rec

def update(id, name, ra, password, birth, idClass):
    rec = db.session.get(Students, id)
    if rec:
        rec.name = name if name is not None else rec.name
        rec.ra = ra if ra is not None else rec.ra
        rec.birth = birth if birth is not None else rec.birth
        rec.idClass = idClass if idClass is not None else rec.idClass
        if password:
            rec.password = password
            
        db.session.commit()
    return rec

def delete(id):
    rec = db.session.get(Students, id)
    if rec:
        db.session.delete(rec)
        db.session.commit()
    return rec